import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from   bokeh.plotting import figure, show


# 한글 폰트 설정
plt.rcParams['font.family'] = "Gothic"
plt.rcParams['axes.unicode_minus'] = False

def connect_db():
    sql = sqlite3.connect('./ahsim.db')
    sql.row_factory = sqlite3.Row
    return sql

with st.sidebar:
    table_sel = st.radio('DB Table Seletct?',('AH2', 'AH8_cs156'),index=1,horizontal=True)
    if table_sel == 'AH2':
        db_table = "AH2"
    else :
        db_table = "AH8_cs156"
        
    fl_sel = st.radio('Simulation Type?',('FL', 'FX'),index=0,horizontal=True)
    if fl_sel == 'FL':
        test_case = "AH_AP1FL"
    else :
        test_case = "AH_AP1FX"

    op_sel = st.radio('Operation Type?',('O1','O2', 'O4','O8'),index=1,horizontal=True)
    if op_sel == 'O1':
        test_case = test_case+"_OP1"
    elif op_sel == 'O2':
        test_case = test_case+"_OP2"
    elif op_sel == 'O4':
        test_case = test_case+"_OP4"
    else: 
        test_case = test_case+"_OP8"
   
    mode_sel = st.radio('Mode Type?',('1Mx1','1Mx2','1Mx4','2Sx1','2Lx1','2Sx2','2Lx2','4Sx1','4Lx1','1Mx8','2Sx4','2Lx4','8Sx1','8Lx1'),index=3)
    if mode_sel == '1Mx1':
        test_case = test_case+"_1Mx1"
    elif mode_sel == '1Mx2':
        test_case = test_case+"_1Mx2"
    elif mode_sel == '1Mx4':
        test_case = test_case+"_1Mx4"    
    elif mode_sel == '2Sx1':
        test_case = test_case+"_2Sx1"
    elif mode_sel == '2Lx1':
        test_case = test_case+"_2Lx1"   
    elif mode_sel == '2Sx2':
        test_case = test_case+"_2Sx2"
    elif mode_sel == '2Lx2':
        test_case = test_case+"_2Lx2"    
    elif mode_sel == '4Sx1':
        test_case = test_case+"_4Sx1"
    elif mode_sel == '4Lx1':
        test_case = test_case+"_4Lx1"   
    elif mode_sel == '1Mx8':
        test_case = test_case+"_1Mx8"    
    elif mode_sel == '2Sx4':
        test_case = test_case+"_2Sx4"
    elif mode_sel == '2Lx4':
        test_case = test_case+"_2Lx4"   
    elif mode_sel == '8Sx1':
        test_case = test_case+"_8Sx1"
    else: 
        test_case = test_case+"_8Lx1"  
        
    pri_sel = st.radio('Primary ?',('P0', 'P1','P2', 'P3','P4', 'P5','P6', 'P7'),index=0,horizontal=True)
    

st.title(f'"{db_table}" C Simulation Result')

db = connect_db()
cur = db.cursor()
sql_cnt_table = f'SELECT COUNT(*) from sqlite_master WHERE type="table" AND name="{db_table}"'
cur.execute(sql_cnt_table)
cnt_table = cur.fetchone()
if cnt_table[0] == 0 :
    st.title(f':red[There is not "{db_table}" in C Simulation Result DB]')
else:
    sql_query_table = f'SELECT id, time, fl, op, mode, mcs, pri, per FROM "{db_table}"'
    cur = db.execute(sql_query_table) 
    results = cur.fetchall()
    st.write(f'SELECTED PER TEST Parameter : :green[{db_table}] :red[{test_case}]\_MCSxx_:red[{pri_sel}]_LGI_STBCx_DOPx_SMTx_D256')    

    sql_mcs_per = f'SELECT mcs,per FROM "{db_table}" WHERE fl = "{fl_sel}" AND op = "{op_sel}" AND mode = "{mode_sel}" AND pri = "{pri_sel}" '
    selected_mcs_per = db.execute(sql_mcs_per)
    results_mcs_per  = selected_mcs_per.fetchall()
    
    if not results_mcs_per:        
        if(op_sel=='O1'):
            if(mode_sel=='1Mx1'):
                st.title(f':red[Selected TEST is not TESTED, yet!]')         
            else:
                st.title(f':blue[Undefined MODE\!]')         
        elif(op_sel=='O2'):       
            if(mode_sel=='1Mx1' or mode_sel=='1Mx2' or mode_sel=='2Sx1' or mode_sel=='2Lx1'):
                st.title(f':red[Selected TEST is not TESTED, yet!]')         
            else:
                st.title(f':blue[Undefined MODE\!]')         
        elif(op_sel=='O4'):       
            if(mode_sel=='1Mx1' or mode_sel=='1Mx2' or mode_sel=='1Mx4'or mode_sel=='2Sx1' or mode_sel=='2Lx1'or \
               mode_sel=='2Sx2' or mode_sel=='2Lx2' or mode_sel=='4Sx1'or mode_sel=='4Lx1'):
                st.title(f':red[Selected TEST is not TESTED, yet!]')         
            else:
                st.title(f':blue[Undefined MODE\!]')         
        else :
            st.title(f':red[Selected TEST is not TESTED, yet!]')                               

    else : 
        df_snr = pd.DataFrame({'SNR': np.arange(0,30,0.5)})
        df_per = pd.DataFrame(results_mcs_per)
    
        column_name = ['SNR']
        for i in range(len(results_mcs_per)):
            per_list = df_per[1][i].replace("\n","").split(' ')          
            df_snr.loc[:,i+1] = pd.DataFrame(per_list)
            column_name.append(df_per[0][i])   
    
        df_snr.columns = column_name 
        df = df_snr.fillna(0.000000)    

        p = figure(
            title = test_case,
            y_axis_type="log",x_range=(0, 30), y_range=(10**-5,1.000),
            x_axis_label='SNR(dB)',
            y_axis_label='PER(Log Scale)')

        p.line(df['SNR'],df['M00'], legend_label='M00', line_width=2,line_color="black", line_dash="solid")
        p.line(df['SNR'],df['M01'], legend_label='M01', line_width=2,line_color="black", line_dash="solid")#dashed")
        p.line(df['SNR'],df['M02'], legend_label='M02', line_width=2,line_color="black", line_dash="solid")#dotted")
        p.line(df['SNR'],df['M03'], legend_label='M03', line_width=2,line_color="black", line_dash="solid")#dotdash")
        p.line(df['SNR'],df['M04'], legend_label='M04', line_width=2,line_color="black", line_dash="solid")#dashdot")
        p.line(df['SNR'],df['M05'], legend_label='M05', line_width=2,line_color="black", line_dash="solid")#solid")
        p.line(df['SNR'],df['M06'], legend_label='M06', line_width=2,line_color="black", line_dash="solid")#dashed")
        p.line(df['SNR'],df['M07'], legend_label='M07', line_width=2,line_color="black", line_dash="solid")#dotted")   
        p.plot.circle(df['SNR'],df['M00'], fill_color="black", line_color='black', size=5)
        p.plot.circle(df['SNR'],df['M01'], fill_color="black", line_color='black', size=5)
        p.plot.circle(df['SNR'],df['M02'], fill_color="black", line_color='black', size=5)
        p.plot.circle(df['SNR'],df['M03'], fill_color="black", line_color='black', size=5)
        p.plot.circle(df['SNR'],df['M04'], fill_color="black", line_color='black', size=5)
        p.plot.circle(df['SNR'],df['M05'], fill_color="black", line_color='black', size=5)
        p.plot.circle(df['SNR'],df['M06'], fill_color="black", line_color='black', size=5)
        p.plot.circle(df['SNR'],df['M07'], fill_color="black", line_color='black', size=5)           
        p.legend.location = "top_right"  
        p.yaxis.ticker.num_minor_ticks = 10
        p.ygrid.minor_grid_line_color = "gray" 
        p.ygrid.minor_grid_line_dash = 'dotted'
        p.ygrid.grid_line_color = "gray"
        p.background_fill_color = (230, 230, 230)
        p.border_fill_color     = (200, 200, 200)
        p.outline_line_color    = (  0,   0,   0)
        st.bokeh_chart(p, use_container_width=True)
        st.write(f'SELECTED PER RESULT:')  
        st.dataframe(df, use_container_width=False)
