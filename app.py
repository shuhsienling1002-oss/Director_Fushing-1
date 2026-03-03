import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. 系統設定 (復興區專屬版)
# ==========================================
st.set_page_config(
    page_title="復興區長者福利試算系統",
    page_icon="⛰️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. 核彈級隱藏工程 (CSS + JavaScript)
# ==========================================
def inject_hide_style():
    # 1. 強力 CSS 隱藏
    hide_css = """
    <style>
        /* 隱藏上方選單與 Header */
        header {visibility: hidden !important; display: none !important;}
        [data-testid="stHeader"] {visibility: hidden !important; display: none !important;}
        
        /* 隱藏底部 Footer */
        footer {visibility: hidden !important; display: none !important;}
        .stFooter {display: none !important;}
        
        /* 隱藏右下角/底部的浮水印 (Hosted with Streamlit) */
        div[class^="viewerBadge"] {visibility: hidden !important; display: none !important;}
        .viewerBadge_container__1QSob {display: none !important;}
        
        /* 隱藏頭像與 Created by */
        div[data-testid="stToolbar"] {display: none !important;}
        div[data-testid="stDecoration"] {display: none !important;}
        div[data-testid="stStatusWidget"] {display: none !important;}
        
        /* 手機版調整 */
        .stApp {margin-top: -80px;} /* 強制往上拉，蓋住可能的殘留 */
    </style>
    """
    st.markdown(hide_css, unsafe_allow_html=True)

    # 2. JavaScript 異步移除 (針對頑強元素)
    # 這段 JS 會每隔 0.5 秒檢查一次頁面，發現浮水印就直接砍掉 DOM 節點
    hide_js = """
    <script>
        function removeWatermarks() {
            // 鎖定所有可能的浮水印 class 關鍵字
            const selectors = [
                'div[class*="viewerBadge"]',
                '[data-testid="stHeader"]',
                'footer',
                'div[data-testid="stToolbar"]'
            ];
            
            selectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    el.style.display = 'none';
                    el.style.visibility = 'hidden';
                    el.innerHTML = ''; // 清空內容
                });
            });
        }
        
        // 頁面加載後執行
        window.addEventListener('load', function() {
            removeWatermarks();
            // 每 500 毫秒再殺一次，確保動態載入的也被刪除
            setInterval(removeWatermarks, 500);
        });
    </script>
    """
    # 將 JS 注入到頁面底部 (height=0 隱藏執行框)
    components.html(hide_js, height=0)

# 執行隱藏指令
inject_hide_style()

# ==========================================
# 3. CSS 美化設計 (視覺優化)
# ==========================================
st.markdown("""
    <style>
    /* === 全站字體與背景 === */
    .stApp {
        background-color: #f8f9fa;
        font-family: "Microsoft JhengHei", sans-serif;
    }
    
    /* === 標題區塊設計 === */
    .header-box {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-title {
        font-size: 28px;
        font-weight: bold;
        margin: 0;
    }
    .header-subtitle {
        font-size: 18px;
        opacity: 0.9;
        margin-top: 5px;
    }
    
    /* === 福利卡片設計 === */
    .benefit-card {
        background-color: white;
        border-left: 5px solid #2E8B57;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .money-tag {
        color: #d63384; 
        font-size: 22px;
        font-weight: 900;
    }
    .location-tag {
        font-size: 14px;
        color: #666;
        background-color: #f1f3f5;
        padding: 2px 8px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. 頁面標題區 (蘇佐璽區長形象)
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">⛰️ 復興區福利小幫手</div>
        <div class="header-subtitle">桃園市復興區長 <b>蘇佐璽</b> 關心您 ❤️</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 5. 輸入區 (條件設定)
# ==========================================
with st.container(border=True):
    st.markdown("### 📝 請勾選長輩狀況")
    
    col_age, col_res = st.columns([1, 2])
    with col_age:
        age = st.number_input("長輩年齡 (歲)", 50, 120, 55)
    with col_res:
        st.info("本系統以 **原住民身分** 為預設計算標準")

    c1, c2 = st.columns(2)
    with c1:
        is_farmer = st.checkbox("🌱 具有農保身分")
        is_low_income = st.checkbox("📉 列冊中低收入戶")
        has_disability = st.checkbox("♿ 領有身障手冊")
    with c2:
        is_owner = st.checkbox("🏠 自有住宅")
        is_renter = st.checkbox("🔑 租賃房屋")
        grandparenting = st.checkbox("👶 協助照顧孫子女")

# ==========================================
# 6. 核心顯示函數
# ==========================================
def show_item(index, name, money, qualify, note, location, highlight=False):
    if qualify:
        border_color = "#2E8B57" # 綠色
        bg_color = "#ffffff"
        
        if highlight:
            border_color = "#FFD700" # 金色
            bg_color = "#fffbea"     # 淡黃底色

        st.markdown(f"""
        <div style="background-color: {bg_color}; border-left: 5px solid {border_color}; padding: 15px; margin-bottom: 12px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-weight: bold; font-size: 18px;">{index}. {name}</div>
                <div class="location-tag">{location}</div>
            </div>
            <div style="margin-top: 8px;">
                <span class="money-tag">{money}</span>
            </div>
            <div style="margin-top: 8px; font-size: 15px; color: #555;">
                💡 {note}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.expander(f"🔒 {index}. {name} (未符條件)", expanded=False):
            st.caption(f"需滿足條件：{note}")
            st.caption(f"承辦單位：{location}")

# ==========================================
# 7. 福利清單
# ==========================================
st.markdown("### 💰 您的專屬福利試算結果")

tabs = st.tabs(["💵 現金津貼", "🩺 醫療照護", "🏠 居住交通", "🛡️ 其他權益"])

with tabs[0]:
    st.caption("每月或每年定期的現金補助")
    show_item(1, "桃園老人三節禮金", "$2,500/每節 (年領$7,500)", (age>=55), "原住民55歲設籍滿6個月", "區公所社會課")
    show_item(2, "桃園重陽敬老金", "$2,500/年", (age>=55), "原住民55歲 (一般65歲)", "區公所社會課")
    show_item(3, "原住民給付 (國保)", "$4,049/月", (55<=age<65), "55-64歲專屬 (與老農互斥)", "區公所原民課")
    show_item(4, "老農津貼", "$8,110/月", (is_farmer and age>=65), "農保年資滿15年", "地區農會")
    show_item(5, "桃園市急難救助", "5,000元至6萬元", True, "申請人設籍本區，發生急難事由3個月以內申請。<br>(1)喪葬補助: 依身分類別審核救助7,000元至6萬元。<br>(2)醫療補助: 依身分類別審核救助5,000元至4萬元。<br>(3)失業或其他原因無法工作: 負擔主要家庭生計者，依身分類別審核救助5,000元至4萬元。<br>(4)財產因故未能及時運用: 依身分類別審核救助5,000元至4萬元。<br>(5)尚未獲得福利補助或保險給付前: 依身分類別審核救助5,000元至4萬元。<br>(6)遭遇其他重大變故: 依身分類別審核救助5,000元至4萬元。", "區公所社會課")
    show_item(6, "弱勢兒少托育(隔代)", "$3,000起/月", (grandparenting and is_low_income), "祖父母照顧孫子女補助", "區公所社會課")

with tabs[1]:
    st.caption("牙齒、健保與輔具補助")
    show_item(7, "桃園原民假牙補助", "最高4.4萬", (age>=55), "需先至診所估價", "區公所原民課")
    show_item(8, "健保費補助", "減免補助", (age>=55), "55-64歲原住民 (系統自動減免)，補助最高上限至地區人口保費", "健保局")
    show_item(9, "成人健康檢查", "免費", (age>=55), "每年一次 (原住民提早至55歲)", "衛生所/特約醫院")
    show_item(10, "身障輔具補助", "全額/部分", has_disability, "助聽器/氣墊床等 (需有有效身心障礙證明)", "區公所社會課")

with tabs[2]:
    st.caption("房屋修繕與交通優惠")
    show_item(11, "復興區敬老愛心卡", "每月1000點", (age>=55), "復興區民專屬福利 (一般區800點)", "區公所社會課", highlight=True)
    show_item(12, "愛心計程車", "點數折抵", (age>=55), "單趟100元以下補36點", "各大車隊")
    show_item(13, "桃園修繕住宅補助", "最高15萬", is_owner, "屋頂/衛浴修繕 (需自有)", "區公所原民課")
    show_item(14, "桃園建購住宅補助", "最高22萬", is_owner, "購買或自建房屋", "區公所原民課")
    show_item(15, "租金補貼 (300億)", "依等級 ($3000起)", is_renter, "租屋者可申請", "線上申請/營建署")

with tabs[3]:
    st.caption("喪葬與法律扶助")
    show_item(16, "農保喪葬津貼", "$153,000", is_farmer, "農民身故 (由家屬請領)", "農會保險部")
    show_item(17, "國保喪葬給付", "約9.8萬", (not is_farmer), "一般國保身故 (由家屬請領)", "勞保局")
    show_item(18, "原住民法律扶助", "律師費全免", True, "訴訟/法律諮詢", "法扶基金會")
    show_item(19, "意外保險 (微型)", "最高30萬", is_low_income, "市府代為投保", "社會局")

# ==========================================
# 8. 底部聯絡區 (純淨版)
# ==========================================
st.markdown("---")
col_footer1, col_footer2 = st.columns(2)

with col_footer1:
    st.markdown("#### 📞 服務專線")
    st.markdown("🔹 **復興區公所**：(03) 382-1500")
    st.markdown("🔹 **市民專線**：1999")

with col_footer2:
    st.markdown("#### 🏥 照護資源")
    st.markdown("🔸 **長照專線**：1966")
    st.markdown("🔸 **復興區衛生所**：(03) 382-2325")

st.markdown("""
    <div style="text-align: center; margin-top: 30px; color: #888; font-size: 12px;">
    ⚠️ 本試算系統僅供參考，實際資格以政府機關最新核定為準。
    </div>
""", unsafe_allow_html=True)
