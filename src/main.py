"""
Academic Analytics
Course: Data St
"""
import os
import sys
import json
me

# Add parent directory to path for imports
sys.path.insert(0, os.path.d))

frs
from src.transfoent
from src.analyze import (compute_stats, k,
                         sers)
from src.reports import (print_sn,
                  n)


def load_con:
main()":
    ain__"__me__ == 
if __nam60)

print("="*s")
    ndco2f} se:.{elapsedn d ilete comp Pipelinef"\n✓int(
    prime() - start_te.time= timpsed    elaing
 timPerformance  
    # )
   v"nts.cst_risk_studeer']}/aoutput_foldaths[', f"{pt_risk_list(aport_at_risk       ex at_risk:
 ist
    ifrt at-risk l
    # Expo
    folder'])hs['output_atcords, ption(rey_secxport_btion
    et by sec# Expor        
.")
ata..Exporting d\n[6/6] "rint(   pport data
 
    # Ex   
 ")rs]}utlie o in od(o, 2) for{[roundes: r gratlies)} ou(outlierlenf"Found {   print()
     od) ---"R Meth(IQliers e Out"\n--- Grad   print(f  
    outliers:ers
    ifrint outli P  
    #ers")
  5 Perform"Top 5], 0[:p_1ent_list(tont_studri    pformers
nt top per    # Pri")
    
isk']})olds['at_re < {thresh(Gradudents "At-Risk St(at_risk, fststudent_li    print__risk:
    f atnts
    i student at-risk
    # Pri   
 stats)ection_mparison(stion_coec_s print
   omparisontion c# Print sec
    
    ribution)ts, distrecords, staummary(print_sry
    umma # Print s    
   orts...")
erating rep/6] Gen[5 print("\ns
   portenerate re    # G 
  
 0)ords, 1rs(recop_performe0 = t_1   top
 mersfor  # Top per
    
  n(records)risoction_compastats = se section_n
   socomparin  # Sectio)
    
   valid_gradestliers(oufind_utliers = 
    oers outli
    # Find
    risk'])at_hresholds['cords, tsk(rey_at_ri= identifsk t_rients
    ask stud-ridentify at 
    # I
   n(records)utiorade_distrib g =istribution   d)
 deslid_grate_stats(va= computs s
    statatistic Compute s
    #
    ot None]is nal_grade'] if r['fin records for r inl_grade'] 'fina[r[s = valid_gradeics
    tistfor stagrades t valid acExtr#     
    cs...")
nalytierforming a P/6]\n[4int("ata
    pr dze   # Analy
 rd)
    ent(recovemute_improent'] = compmprovemd['i       recor records:
 incord for reic
    ment metrd improveAd   
    # le)
 cas, grade_shtds, weigs(recorted_fieldmpu = add_co
    records")s...nsformationdes and traputing gra6] Com"\n[3/print(   ata
  Transform d
    #ds")
    dent recorcords)} stulen(relly loaded {ccessfuf"Su
    print(or}")
    - {err   print(f"           rs:
erro in ror    for er  ion:")
  estg ingrs durings/ErronWarnin"\rint(f  prs:
      
    if erro    .csv")
putfolder']}/in'input_"{paths[fd_csv(rors = reards, er")
    recocsv...ut.}/inpolder']nput_fths['i {pafrom data /6] Readingint(f"\n[2 prst data
   nge# I     
  ]
 scale'fig['grade_ale = conade_sc']
    gr'paths= config[s  path
   lds']hreshog['t = confihresholdshts']
    t'weigs = config[ight
    we
          return
  Exiting.")tion.  configura to load"Failedt(prin     ig:
   ot confif n()
    configd_= loaig ")
    conftion... configuraading\n[1/6] Lorint("
    ponfiguration c# Load
    
    0)"="*6  print( LITE")
   ANALYTICSCADEMIC   print("A)
 "="*60t( 
    prine()
    time.timt_time =  star""
  " execution.n pipeline""Mai):
    "main(
def one

 N      return")
  e}nfig: {ng coloadi"Error    print(f      e:
eption aspt Excf)
    exced(n.loareturn jso        f:
     ath, 'r') as(config_p   with open   try:
  
    file.""" from JSON figuration""Load con  "  dictjson') -> = 'config.: str pathig(config_f
