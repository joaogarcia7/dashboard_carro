import streamlit as st
import pandas as pd

st.set_page_config(page_title="Concessionária - Vendas de Carros", page_icon="---", layout="wide")

st.markdown(
    """
    <style>
    * {
        border-radius: 0px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

CATALOGO_CARROS = {
    "Fiat Strada Endurance 1.3": {"categoria": "Picape", "preco": 105990.00},
    "VW Polo Track 1.0": {"categoria": "Hatch", "preco": 89990.00},
    "Chevrolet Onix LT 1.0 Turbo": {"categoria": "Hatch", "preco": 102500.00},
    "Hyundai Creta Action 1.6": {"categoria": "SUV", "preco": 119990.00},
    "Toyota Corolla XEi 2.0": {"categoria": "Sedan", "preco": 161990.00},
    "Jeep Compass Longitude T270": {"categoria": "SUV", "preco": 194990.00},
    "BYD Dolphin Mini": {"categoria": "Elétrico", "preco": 115800.00},
    "Ford Ranger XLT 2.0 Diesel": {"categoria": "Picape", "preco": 289990.00},
}

if "carrinho_carros" not in st.session_state:
    st.session_state.carrinho_carros = []

st.title("Dashboard de Concessionária - Ponto de Venda")
st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Seleção de Veículos")
    
    with st.form("form_veiculo", clear_on_submit=False):
        carro_nome = st.selectbox("Escolha o Modelo do Veículo", list(CATALOGO_CARROS.keys()))
        categoria_carro = CATALOGO_CARROS[carro_nome]["categoria"]
        preco_unit = CATALOGO_CARROS[carro_nome]["preco"]
        
        st.caption(f"Categoria: **{categoria_carro}** | Preço de Tabela: **R$ {preco_unit:,.2f}**")
        
        quantidade = st.number_input("Quantidade (Unidades / Frota)", min_value=1, value=1, step=1)
        
        btn_adicionar = st.form_submit_button("Adicionar ao Pedido", use_container_width=True)
        
        if btn_adicionar:
            subtotal = preco_unit * quantidade
            st.session_state.carrinho_carros.append({
                "Veículo": carro_nome,
                "Categoria": categoria_carro,
                "Preço Unit. (R$)": preco_unit,
                "Qtd": quantidade,
                "Subtotal (R$)": subtotal
            })
            st.success(f"**{carro_nome}** adicionado ao pedido com sucesso!")

    st.subheader("Pedido Atual")
    if st.session_state.carrinho_carros:
        df_carrinho = pd.DataFrame(st.session_state.carrinho_carros)
        
        st.dataframe(
            df_carrinho,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Preço Unit. (R$)": st.column_config.NumberColumn(
                    "Preço Unit.",
                    format="R$ %.2f"
                ),
                "Subtotal (R$)": st.column_config.NumberColumn(
                    "Subtotal",
                    format="R$ %.2f"
                )
            }
        )
        
        if st.button("Limpar Pedido", use_container_width=True):
            st.session_state.carrinho_carros = []
            st.rerun()
    else:
        st.info("Nenhum veículo selecionado. Adicione veículos acima para montar o pedido.")

with col2:
    st.subheader("Faturamento e Fechamento")
    
    total_compra = sum(item["Subtotal (R$)"] for item in st.session_state.carrinho_carros)
    
    st.metric(label="VALOR TOTAL DO PEDIDO", value=f"R$ {total_compra:,.2f}")
    
    st.markdown("---")
    
    valor_recebido = st.number_input(
        "Valor Transferido / Pago pelo Cliente (R$)",
        min_value=0.0,
        value=0.0,
        step=1000.0,
        format="%.2f"
    )
    
    if total_compra == 0:
        st.warning("Adicione veículos ao pedido antes de prosseguir com o faturamento.")
    else:
        troco = valor_recebido - total_compra
        
        if valor_recebido == 0:
            st.info("Aguardando a confirmação da transferência ou pagamento...")
        elif valor_recebido < total_compra:
            falta = total_compra - valor_recebido
            st.error(f"**Valor Insuficiente!** Faltam **R$ {falta:,.2f}** para quitar o pedido.")
        else:
            st.success("**Faturamento Concluído! Veículo(s) liberado(s) para entrega.**")
            st.metric(label="SALDO / TROCO A DEVOLVER", value=f"R$ {troco:,.2f}")
            
            with st.expander("Ver Nota Fiscal / Comprovante da Venda"):
                total_veiculos = sum(item["Qtd"] for item in st.session_state.carrinho_carros)
                st.write(f"**Modelos Distintos no Pedido:** {len(st.session_state.carrinho_carros)}")
                st.write(f"**Total de Veículos Adquiridos:** {total_veiculos}")
                st.write(f"**Valor Total da Nota:** R$ {total_compra:,.2f}")
                st.write(f"**Valor Recebido:** R$ {valor_recebido:,.2f}")
                st.write(f"**Troco / Estorno:** R$ {troco:,.2f}")
            
            if st.button("Finalizar Venda e Atender Novo Cliente", type="primary", use_container_width=True):
                st.session_state.carrinho_carros = []
                st.rerun()
