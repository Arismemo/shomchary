import streamlit as st

if 'single_machine_cost' not in st.session_state:
    st.session_state['single_machine_cost'] = 0.0

if 'single_material_cost' not in st.session_state:
    st.session_state['single_material_cost'] = 0.0


tab1, tab2 = st.tabs(["计算成本", "设置"])

with tab2:
    with st.form('配置信息'):


        st.header('原料配方')
        with st.container():
            with st.container():
                col1,col2 = st.columns(2)
                with col1:
                    oil_weight = st.number_input('油 kg', value = 1000)
                with col2:
                    oil_price = st.number_input('单价 元/kg', value = 12.3, key=1)

            with st.container():
                col1,col2 = st.columns(2)
                with col1:
                    powder_weight = st.number_input('粉 kg', value = 1000)
                with col2:
                    powder_price = st.number_input('单价 元/kg', value = 8.65, key = 2)

            with st.container():
                col1,col2 = st.columns(2)
                with col1:
                    calcium_weight = st.number_input('钙 kg',value = 300)
                with col2:
                    calcium_price = st.number_input('单价 元/kg', value = 1.1, key = 3)

            with st.container():
                col1,col2 = st.columns(2)
                with col1:
                    color_paste_weight = st.number_input('色膏 kg', value = 47)
                with col2:
                    color_paste_price = st.number_input('单价 元/kg', value = 60, key=4)

        st.header('其它')
        with st.container():
            col1,col2,col3,col4=st.columns(4)
            raw_material_density = col1.number_input(label="原料密度 g/ml", value=1.65714286)
            unit_count = col2.number_input(label="机台数量 /台", value=18)
            unit_price = col3.number_input(label="机台单价 /元", value=40000)
            electric_charge = col4.number_input(label="电费 /元", value=20000)

        with st.container():
            col1,col2,col3,col4,col5,col6=st.columns(6)
            machine_wage = col1.number_input(label="机台工资 /元", value=115200)
            transfer_wage = col2.number_input(label="调机工资 /元", value=19000)
            color_mix_wage = col3.number_input(label="调色工资 /元", value=13000)
            documentary_wage = col4.number_input(label="跟单工资 /元", value=7000)
            administrative_wage = col5.number_input(label="管理工资 /元", value=24000)
            rent = col6.number_input(label="房租 /元", value=5000)



        submitted = st.form_submit_button("设置")
        if submitted:
            st.session_state['single_machine_cost'] = (machine_wage + transfer_wage + color_mix_wage + documentary_wage + administrative_wage + rent + (unit_count * unit_price) / 5 / 12 + electric_charge) / unit_count
            st.session_state['single_material_cost'] = (oil_weight*oil_price + powder_weight*powder_price + calcium_weight*calcium_price + color_paste_weight*color_paste_price) / (oil_weight* 1000 + powder_weight* 1000 + calcium_weight* 1000 + color_paste_weight* 1000)  
            st.divider()
            st.success("单机台月成本: {:.2f} 元/月".format(st.session_state['single_machine_cost']), icon="✅")
            st.success("1克颜料成本: {:.4f} 元/月".format(st.session_state['single_material_cost']), icon="✅")


if st.session_state['single_machine_cost'] == 0:
    st.session_state['single_machine_cost'] = (machine_wage + transfer_wage + color_mix_wage + documentary_wage + administrative_wage + rent + (unit_count * unit_price) / 5 / 12 + electric_charge) / unit_count

if st.session_state['single_material_cost'] == 0:
    st.session_state['single_material_cost'] = (oil_weight*oil_price + powder_weight*powder_price + calcium_weight*calcium_price + color_paste_weight*color_paste_price) / (oil_weight* 1000 + powder_weight* 1000 + calcium_weight* 1000 + color_paste_weight* 1000)

with tab1:
    with st.form('输入信息'):

        with st.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                length = st.number_input(label="长 /cm", min_value=0.0, max_value=30.0, value=2.5, step=0.1)

            with col2:
                width = st.number_input(label="宽 /cm", min_value=0.0, max_value=30.0, value=2.5, step=0.1)

            with col3:
                height = st.number_input(label="高 /cm", min_value=0.0, max_value=30.0, value=0.3, step=0.1)

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                machine_time_per_unit_product = st.number_input(label="单位产品机器耗时 /s：", min_value=0.0, max_value=30.0, value=5.0, step=0.1)

            with col2:
                labor_time_per_unit_product = st.number_input(label="单位产品人工耗时 /s", min_value=0.0, max_value=30.0, value=0.5, step=0.1)

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                single_machine_expected_profit = st.number_input(label="单机台月预计盈利 /元：", min_value=0, max_value=300000, value=5000, step=1000)


        submitted = st.form_submit_button("计算")
        if submitted:
            product_volume = length * width * height
            product_mass = product_volume * raw_material_density

            # 单个产品原料成本
            product_mass_price = product_mass * st.session_state['single_material_cost']

            day_work_hour_count = 21.5
            month_work_day_count = 29

            # 单机台月产量
            monthly_output = (month_work_day_count * month_work_day_count * 60 * 60) /  (machine_time_per_unit_product + labor_time_per_unit_product)
            
            # 单个产品固定成本
            fixed_price = st.session_state['single_machine_cost'] / monthly_output

            # 单个产品总成本 = 单个产品原料成本 + 单个产品固定成本
            cost_price = product_mass_price + fixed_price

            profit = single_machine_expected_profit / monthly_output

            offer_price = cost_price + profit
            st.write("成本：{:.4f}, 报价：{:.4f}".format(cost_price, offer_price))



