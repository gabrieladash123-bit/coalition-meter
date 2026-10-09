import ast
import hashlib
import itertools
import json
import re
from fractions import Fraction
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[2]
REPO='gabrieladash123-bit/coalition-meter'
TABLES={'additive':[0,6,12,18,18,24,30,36],'shared':[0,10,10,14,10,14,14,18],'unstable':[0,10,10,10,10,10,10,24],'missing':[0,10,10,14,10,14,14,None],'nonmonotone':[0,10,10,14,10,14,14,9]}
BODY={name:(ROOT/'records'/f'{name}.json').read_bytes() for name in TABLES}

def source(name):
    return f"https://raw.githubusercontent.com/{REPO}/{'a'*40}/records/{name}.json",hashlib.sha256(BODY[name]).hexdigest()

def report(name):
    anchors=list(range(len(re.split(r'(?<=[.!?])\s+',json.loads(BODY[name])['tariff']))))
    return {'coalitions':[{'mask':mask,'decision':'UNKNOWN' if cost is None else 'KNOWN','cost':cost,'anchors':anchors} for mask,cost in enumerate(TABLES[name][1:],1)]}

def mock(vm,name,leader=None,own=None,anchors=None,body=None):
    vm.clear_mocks()
    vm.mock_web(re.escape(source(name)[0]),{'status':200,'body':BODY[name] if body is None else body})
    vm.mock_llm(r'.*COALITIONMETER-LEADER.*',json.dumps(report(name) if leader is None else leader))
    vm.mock_llm(r'.*COALITIONMETER-VALIDATOR.*',json.dumps(report(name) if own is None else own))
    valid=[True]*7 if anchors is None else anchors
    vm.mock_llm(r'.*COALITIONMETER-ANCHORS.*',json.dumps({'checks':[{'mask':i,'valid':value,'reason':'Referenced tariff rules substantiate the proposed total or absence.'} for i,value in enumerate(valid,1)]}))

@pytest.fixture
def meter(direct_deploy):
    return direct_deploy(str(ROOT/'contracts/coalition_meter.py'),REPO)

def run(c,vm,name):
    mock(vm,name);c.allocate(*source(name))
    return c.get_state()['batches'][-1]['result']

def test_additive_shares_equal_standalone_prices(meter,direct_vm):
    r=run(meter,direct_vm,'additive')
    assert r['status']=='STABLE' and r['shares_numerator']==[36,72,108]
    assert r['rounded_preview']==[6,12,18] and not r['core_violations']

def test_economies_shared_symmetrically(meter,direct_vm):
    r=run(meter,direct_vm,'shared')
    assert r['status']=='STABLE' and r['shares_numerator']==[36]*3
    assert r['rounded_preview']==[6]*3

def test_shapley_budget_balance_does_not_imply_core_stability(meter,direct_vm):
    r=run(meter,direct_vm,'unstable')
    assert r['status']=='UNSTABLE' and r['shares_numerator']==[48]*3
    assert [w['mask'] for w in r['core_violations']]==[3,5,6]
    assert all(w['excess_numerator']==36 for w in r['core_violations'])

def test_missing_quote_prevents_entire_allocation(meter,direct_vm):
    r=run(meter,direct_vm,'missing')
    assert r['status']=='REVIEW' and r['unknown']==[7]
    assert r['shares_numerator']==r['rounded_preview']==[]

def test_explicit_unknown_omitted_cost_normalizes_to_null(meter,direct_vm):
    proposed=report('missing');del proposed['coalitions'][6]['cost']
    mock(direct_vm,'missing',leader=proposed,own=proposed)
    meter.allocate(*source('missing'))
    r=meter.get_state()['batches'][0]
    assert r['report']['coalitions'][6]['cost'] is None
    assert r['result']['status']=='REVIEW' and r['result']['shares_numerator']==[]
    assert direct_vm.run_validator() is True

def test_promotional_price_is_preserved_and_domain_violation_exposed(meter,direct_vm):
    r=run(meter,direct_vm,'nonmonotone')
    assert r['costs'][7]==9 and r['status']=='INCONSISTENT'
    assert len(r['monotonicity_violations'])==6
    assert r['shares_numerator']==[]

def test_validator_independent_agreement(meter,direct_vm):
    run(meter,direct_vm,'shared')
    assert direct_vm.run_validator() is True

@pytest.mark.parametrize('name,index,decision,cost',[('shared',2,'KNOWN',13),('missing',6,'KNOWN',18),('shared',6,'UNKNOWN',None)])
def test_validator_exact_cost_and_unknown_gate(meter,direct_vm,name,index,decision,cost):
    run(meter,direct_vm,name)
    own=report(name);own['coalitions'][index].update(decision=decision,cost=cost)
    mock(direct_vm,name,own=own)
    assert direct_vm.run_validator() is False

def test_validator_refetch_hash_binding(meter,direct_vm):
    run(meter,direct_vm,'shared');mock(direct_vm,'shared',body=BODY['shared']+b' ')
    assert direct_vm.run_validator() is False

def test_validator_substantive_quote_check(meter,direct_vm):
    run(meter,direct_vm,'missing');mock(direct_vm,'missing',anchors=[True]*6+[False])
    assert direct_vm.run_validator() is False

@pytest.mark.parametrize('kind',['omitted','reordered','boolcost','unknown-cost','wrong-quote','duplicate-anchor','bool-anchor'])
def test_malformed_report_atomic_revert(meter,direct_vm,kind):
    bad=report('shared')
    if kind=='omitted':bad['coalitions'].pop()
    if kind=='reordered':bad['coalitions'].reverse()
    if kind=='boolcost':bad['coalitions'][0]['cost']=True
    if kind=='unknown-cost':bad['coalitions'][0]['decision']='UNKNOWN'
    if kind=='wrong-quote':bad['coalitions'][0]['anchors']=[999]
    if kind=='duplicate-anchor':bad['coalitions'][0]['anchors']=[0,0]
    if kind=='bool-anchor':bad['coalitions'][0]['anchors']=[True]
    mock(direct_vm,'shared',leader=bad)
    with direct_vm.expect_revert():meter.allocate(*source('shared'))
    assert meter.get_state()['batches']==[]

def test_duplicate_source_reverts(meter,direct_vm):
    run(meter,direct_vm,'shared')
    with direct_vm.expect_revert('Duplicate source'):meter.allocate(*source('shared'))

def test_unpinned_source_reverts(meter,direct_vm):
    url,sha=source('shared')
    with direct_vm.expect_revert('pinned publisher'):meter.allocate(url.replace('a'*40,'main'),sha)

def test_bad_source_bytes_revert(meter,direct_vm):
    mock(direct_vm,'shared',body=BODY['shared']+b' ')
    with direct_vm.expect_revert('commitment mismatch'):meter.allocate(*source('shared'))

def test_duplicate_json_key_reverts(meter,direct_vm):
    body=BODY['shared'].replace(b'"tariff":',b'"tariff":"duplicate", "tariff":')
    mock(direct_vm,'shared',body=body)
    with direct_vm.expect_revert('Duplicate JSON'):meter.allocate(source('shared')[0],hashlib.sha256(body).hexdigest())

def pure_compile():
    tree=ast.parse((ROOT/'contracts/coalition_meter.py').read_text())
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='compile_allocation']
    ns={'itertools':itertools,'fail':lambda message:(_ for _ in ()).throw(AssertionError(message))}
    exec(compile(ast.Module(body=funcs,type_ignores=[]),'allocation','exec'),ns)
    return ns['compile_allocation']

def table_report(costs):
    return {'coalitions':[{'mask':i,'decision':'KNOWN','cost':v} for i,v in enumerate(costs[1:],1)]}

def independent_shares(c):
    result=[]
    for member in range(3):
        bit=1<<member
        other=[1<<j for j in range(3) if j!=member]
        x,y=other
        result.append(Fraction(c[bit],3)+Fraction(c[bit|x]-c[x],6)+Fraction(c[bit|y]-c[y],6)+Fraction(c[7]-c[x|y],3))
    return result

def test_exhaustive_2187_cost_tables_budget_core_and_domain():
    compile=pure_compile()
    for values in itertools.product(range(3),repeat=7):
        c=[0,*values];r=compile(table_report(c))
        bad=[(a,b) for a in range(8) for b in range(8) if a!=b and a&b==a and c[a]>c[b]]
        if bad:
            assert r['status']=='INCONSISTENT'
            assert [(v['subset'],v['superset']) for v in r['monotonicity_violations']]==bad
            continue
        exact=independent_shares(c)
        assert [Fraction(x,6) for x in r['shares_numerator']]==exact
        assert sum(exact)==c[7] and min(exact)>=0
        assert sum(r['rounded_preview'])==c[7]
        rounded=r['rounded_preview']
        rounded_bad=[m for m in range(1,7) if sum(rounded[i] for i in range(3) if m&(1<<i))>c[m]]
        assert [w['mask'] for w in r['rounded_core_violations']]==rounded_bad
        expected=[m for m in range(1,7) if sum(exact[i] for i in range(3) if m&(1<<i))>c[m]]
        assert [w['mask'] for w in r['core_violations']]==expected
        assert r['status']==('UNSTABLE' if expected else 'STABLE')
        if not expected:assert not rounded_bad
        for witness in r['core_violations']:
            assert witness['charge_numerator']-witness['standalone_numerator']==witness['excess_numerator']>0

def test_fractional_symmetry_is_not_replaced_by_rounding():
    r=pure_compile()(table_report([0,1,1,1,1,1,1,1]))
    assert r['shares_numerator']==[2,2,2]
    assert r['rounded_preview']==[1,0,0]
    assert r['status']=='STABLE'

def test_dummy_member_has_zero_share():
    r=pure_compile()(table_report([0,2,3,5,0,2,3,5]))
    assert r['shares_numerator']==[12,18,0]

def test_rounding_cannot_hide_authoritative_instability():
    r=pure_compile()(table_report([0,0,0,1,1,1,1,1]))
    assert r['shares_numerator']==[1,1,4] and r['status']=='UNSTABLE'
    assert [w['mask'] for w in r['core_violations']]==[1,2]
    assert r['rounded_preview']==[0,0,1] and r['rounded_core_violations']==[]
