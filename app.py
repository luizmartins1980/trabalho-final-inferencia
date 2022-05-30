import streamlit as st
from streamlit_option_menu import option_menu
import apps.tratamentoBase
import apps.analiseCurso
import apps.inferenciaCurso

st.set_page_config()

with st.sidebar:
    escolha = option_menu("Menu", 
                        
                        ["Inferência por Curso", 
                        "Tratamento Base Dados", 
                        "Análise por Curso"
                        ],

                         icons=["house", "file-bar-graph",  "bar-chart"], #https://icons.getbootstrap.com/
                         
                         menu_icon="menu-button-wide", 
                         
                         default_index=0,
                         
                         styles={
                                    "container": {"padding": "5!important", "background-color": "#E1117"},
                                    "icon": {"color": "#FF4B4B", "font-size": "25px"}, 
                                    
                                    "nav-link": {"font-size": "12px", "text-align": "left", "margin":"0px", "--hover-color": "#262730", "icon" : "#FF4B4B"},
                                    "nav-link-selected": {"background-color": "#262730"},
                                }

                        )


if  escolha == "Tratamento Base Dados":
    apps.tratamentoBase.tratamentoBase()

elif  escolha == "Inferência por Curso":
    apps.inferenciaCurso.inferenciaCurso()

elif  escolha == "Análise por Curso":
    apps.analiseCurso.analiseCurso()

    