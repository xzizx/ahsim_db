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
    st.sidebar.header('Select Target')
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

    op_sel = st.radio('Operation Type?',('O1', 'O2', 'O4','O8'),index=1,horizontal=True)
    if op_sel == 'O1':
        test_case = test_case+"_OP1"
    elif op_sel == 'O2':
        test_case = test_case+"_OP2"
    elif op_sel == 'O4':
        test_case = test_case+"_OP4"
    else: 
        test_case = test_case+"_OP8"
   
    mode_sel = st.radio('Mode Type?',('1Mx1','1Mx2','1Mx4','2Sx1','2Lx1','2Sx2','2Lx2','4Sx1','4Lx1','1Mx8','2Sx4','2Lx4','8Sx1','8Lx1'),index=3,horizontal=True)
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
    
    comp_sel1 = st.selectbox('Compare FL/FX', ('FL', 'FX'),index=0)
    comp_sel2 = st.selectbox('Compare Operating', ('O1', 'O2', 'O4', 'O8'),index=1)
    comp_sel3 = st.selectbox('Compare Mode', ('1Mx1','1Mx2','1Mx4','2Sx1','2Lx1','2Sx2','2Lx2','4Sx1','4Lx1','1Mx8','2Sx4','2Lx4','8Sx1','8Lx1'),index=4)    
    comp_sel4 = st.selectbox('Compare Primary', ('P0', 'P1','P2', 'P3','P4', 'P5','P6', 'P7'),index=0)    

st.title(f'"{db_table}" C Simulation Result')

db = connect_db()
cur = db.cursor()
sql_cnt_table = f'SELECT COUNT(*) from sqlite_master WHERE type="table" AND name="{db_table}"'
cur.execute(sql_cnt_table)
cnt_table = cur.fetchone()
if cnt_table[0] == 0 :
    st.title(f':red[There is not "{db_table}" in C Simulation Result DB]')
else:
    #sql_query_table = f'SELECT id, time, fl, op, mode, mcs, pri, per FROM "{db_table}"'
    #cur = db.execute(sql_query_table) 
    #results = cur.fetchall()
    st.write(f':red[PER TEST] Selected Parameter : AH_AP1:red[{fl_sel}]\_:red[{op_sel}]\_:red[{mode_sel}]\_MCSxx_:red[{pri_sel}]_LGI_STBCx_DOPx_SMTx_D256')  
    st.write(f':blue[Compare] Selected Parameter : AH_AP1:blue[{comp_sel1}]\_:blue[{comp_sel2}]\_:blue[{comp_sel3}]\_MCSxx_:blue[{comp_sel4}]_LGI_STBCx_DOPx_SMTx_D256') 
    
    sql_mcs_per = f'SELECT DISTINCT mcs,per FROM "{db_table}" WHERE fl = "{fl_sel}" AND op = "{op_sel}" AND mode = "{mode_sel}" AND pri = "{pri_sel}" ORDER BY mcs '
    selected_mcs_per = db.execute(sql_mcs_per)
    results_mcs_per  = selected_mcs_per.fetchall()
    
    sql_comp_per = f'SELECT DISTINCT mcs,per FROM "{db_table}" WHERE fl = "{comp_sel1}" AND op = "{comp_sel2}" AND mode = "{comp_sel3}" AND pri = "{comp_sel4}" ORDER BY mcs '
    selected_comp_per = db.execute(sql_comp_per)
    results_comp_per  = selected_comp_per.fetchall()
    
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
             st.write(f':red[Selected TEST is not TESTED, yet!]')                               

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
        
        if results_comp_per :
            df_snr_comp = pd.DataFrame({'SNR': np.arange(0,30,0.5)})
            df_per_comp = pd.DataFrame(results_comp_per)
            comp_column_name = ['SNR']
            for i in range(len(results_comp_per)):
                comp_list = df_per_comp[1][i].replace("\n","").split(' ')          
                df_snr_comp.loc[:,i+1] = pd.DataFrame(comp_list)    
                comp_column_name.append(df_per_comp[0][i])       
            df_snr_comp.columns = comp_column_name 
            df_comp = df_snr_comp.fillna(0.000000)                       

        p = figure(
            title = test_case,
            y_axis_type="log",x_range=(0, 30), y_range=(10**-5,1.000),
            x_axis_label='SNR(dB)',
            y_axis_label='PER(Log Scale)')
        if 'M10' in df.columns :
            p.line(df['SNR'],df['M10'], legend_label='M10', line_width=1,line_color="magenta", line_dash="solid")        
            p.plot.circle(df['SNR'],df['M10'], fill_color="magenta", line_color='magenta', size=7)
        p.line(df['SNR'],df['M00'], legend_label='M00', line_width=2,line_color="red",      line_dash="solid")
        p.line(df['SNR'],df['M01'], legend_label='M01', line_width=2,line_color="orange",   line_dash="solid")
        p.line(df['SNR'],df['M02'], legend_label='M02', line_width=2,line_color="yellow",   line_dash="solid")
        p.line(df['SNR'],df['M03'], legend_label='M03', line_width=2,line_color="lime",     line_dash="solid")
        p.line(df['SNR'],df['M04'], legend_label='M04', line_width=2,line_color="blue",     line_dash="solid")
        p.line(df['SNR'],df['M05'], legend_label='M05', line_width=2,line_color="navy",     line_dash="solid")
        p.line(df['SNR'],df['M06'], legend_label='M06', line_width=2,line_color="blueviolet",line_dash="solid")
        p.line(df['SNR'],df['M07'], legend_label='M07', line_width=2,line_color="black",     line_dash="solid")
        p.plot.circle(df['SNR'],df['M00'], fill_color='red',        line_color='red',       size=7)    
        p.plot.circle(df['SNR'],df['M01'], fill_color='orange',     line_color='orange',    size=7)    
        p.plot.circle(df['SNR'],df['M02'], fill_color='yellow',     line_color='yellow',    size=7)    
        p.plot.circle(df['SNR'],df['M03'], fill_color='lime',       line_color='lime',      size=7)    
        p.plot.circle(df['SNR'],df['M04'], fill_color='blue',       line_color='blue',      size=7)    
        p.plot.circle(df['SNR'],df['M05'], fill_color='navy',       line_color='navy',      size=7)    
        p.plot.circle(df['SNR'],df['M06'], fill_color='blueviolet', line_color='blueviolet',size=7)    
        p.plot.circle(df['SNR'],df['M07'], fill_color='black',      line_color='black',     size=7)       

        if results_comp_per :
            if 'M10' in df_comp.columns :
                p.line(df_comp['SNR'],df_comp['M10'], legend_label='C_M10', line_width=2,line_color="magenta", line_dash="dotted")
                p.plot.circle(df['SNR'],df_comp['M10'], fill_color="magenta", line_color='magenta', size=7)
            p.line(df_comp['SNR'],df_comp['M00'], legend_label='C_M00', line_width=2,line_color="red",      line_dash="dotted")
            p.line(df_comp['SNR'],df_comp['M01'], legend_label='C_M01', line_width=2,line_color="orange",   line_dash="dotted")
            p.line(df_comp['SNR'],df_comp['M02'], legend_label='C_M02', line_width=2,line_color="yellow",   line_dash="dotted")
            p.line(df_comp['SNR'],df_comp['M03'], legend_label='C_M03', line_width=2,line_color="lime",     line_dash="dotted")
            p.line(df_comp['SNR'],df_comp['M04'], legend_label='C_M04', line_width=2,line_color="blue",     line_dash="dotted")
            p.line(df_comp['SNR'],df_comp['M05'], legend_label='C_M05', line_width=2,line_color="navy",     line_dash="dotted")
            p.line(df_comp['SNR'],df_comp['M06'], legend_label='C_M06', line_width=2,line_color="blueviolet",line_dash="dotted")
            p.line(df_comp['SNR'],df_comp['M07'], legend_label='C_M07', line_width=2,line_color="black",     line_dash="dotted")
            p.plot.triangle(df_comp['SNR'],df_comp['M00'], fill_color='red',        line_color='red',       size=7)
            p.plot.triangle(df_comp['SNR'],df_comp['M01'], fill_color='orange',     line_color='orange',    size=7)
            p.plot.triangle(df_comp['SNR'],df_comp['M02'], fill_color='yellow',     line_color='yellow',    size=7)
            p.plot.triangle(df_comp['SNR'],df_comp['M03'], fill_color='lime',       line_color='lime',      size=7)
            p.plot.triangle(df_comp['SNR'],df_comp['M04'], fill_color='blue',       line_color='blue',      size=7)
            p.plot.triangle(df_comp['SNR'],df_comp['M05'], fill_color='navy',       line_color='navy',      size=7)
            p.plot.triangle(df_comp['SNR'],df_comp['M06'], fill_color='blueviolet', line_color='blueviolet',size=7)
            p.plot.triangle(df_comp['SNR'],df_comp['M07'], fill_color='black',      line_color='black',     size=7)    
               
        p.legend.location = "bottom_right"  
        p.legend.title = "MCS"  
        p.yaxis.ticker.num_minor_ticks = 10
        p.ygrid.minor_grid_line_color = "black" 
        p.ygrid.minor_grid_line_dash = 'dotted'
        p.ygrid.grid_line_color = "black"
        p.background_fill_color = (120, 120, 120)
        p.border_fill_color     = (200, 200, 200)
        p.outline_line_color    = (  0,   0,   0)
        st.bokeh_chart(p, use_container_width=True)
        if not results_comp_per :            
            st.write(f':blue[Compare is not TESTED, yet!] or :blue[Undefined MODE\!]')               
        st.write(f'PER TEST RESULT:')  
        st.dataframe(df, use_container_width=False)
        
        if results_comp_per :                    
            st.write(f'Compare RESULT:')  
            st.dataframe(df_comp, use_container_width=False)
        
