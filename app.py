<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>復興區長者福利試算系統</title>
    <style>
        /* === 核心設計風格 === */
        :root {
            --primary-color: #2E8B57; /* 復興區綠 */
            --secondary-color: #3CB371;
            --highlight-color: #d63384; /* 金額桃紅 */
            --bg-color: #f8f9fa;
        }

        body {
            font-family: "Microsoft JhengHei", "Heiti TC", sans-serif;
            background-color: var(--bg-color);
            margin: 0;
            padding: 0;
            color: #333;
            padding-bottom: 60px; /* 預留底部空間 */
        }

        /* === 頂部標題區 (蘇佐璽區長形象) === */
        .header-box {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            padding: 30px 20px 40px 20px;
            color: white;
            text-align: center;
            border-bottom-left-radius: 30px;
            border-bottom-right-radius: 30px;
            box-shadow: 0 4px 10px rgba(46, 139, 87, 0.3);
            margin-bottom: -30px; /* 讓內容卡片往上疊 */
        }
        .header-title { font-size: 24px; font-weight: bold; margin-bottom: 5px; }
        .header-subtitle { font-size: 16px; opacity: 0.95; }
        .mayor-name { font-weight: 900; font-size: 18px; border-bottom: 2px solid rgba(255,255,255,0.5); padding-bottom: 2px;}

        /* === 內容容器 === */
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 0 15px;
        }

        /* === 輸入卡片 === */
        .input-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 18px;
            font-weight: bold;
            color: var(--primary-color);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .section-title::before {
            content: '';
            display: inline-block;
            width: 5px;
            height: 20px;
            background-color: var(--primary-color);
            margin-right: 10px;
            border-radius: 3px;
        }

        /* === 表單元件 === */
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        
        .age-input-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 18px;
            outline: none;
            transition: border-color 0.3s;
        }
        input[type="number"]:focus { border-color: var(--primary-color); }

        .checkbox-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .checkbox-item {
            display: flex;
            align-items: center;
            background: #f9f9f9;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 15px;
        }
        .checkbox-item input { margin-right: 10px; transform: scale(1.2); accent-color: var(--primary-color); }

        /* === 標籤切換 (Tabs) === */
        .tabs {
            display: flex;
            background: white;
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            overflow-x: auto;
        }
        .tab-btn {
            flex: 1;
            border: none;
            background: none;
            padding: 10px 5px;
            font-size: 15px;
            color: #666;
            cursor: pointer;
            border-radius: 8px;
            white-space: nowrap;
        }
        .tab-btn.active {
            background-color: var(--primary-color);
            color: white;
            font-weight: bold;
        }

        /* === 福利結果卡片 === */
        .benefit-list { display: none; }
        .benefit-list.active { display: block; animation: fadeIn 0.5s; }

        .result-card {
            background: white;
            border-left: 5px solid var(--primary-color);
            padding: 15px;
            margin-bottom: 12px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            position: relative;
        }
        /* 重點項目高亮 (如復興區敬老卡) */
        .result-card.highlight {
            border-left-color: #FFD700;
            background-color: #fffbea;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .benefit-name { font-size: 17px; font-weight: bold; color: #333; }
        .location-tag { 
            font-size: 12px; color: #666; 
            background: #f0f0f0; padding: 3px 8px; border-radius: 10px; 
        }
        .money-text { font-size: 20px; font-weight: 900; color: var(--highlight-color); margin-bottom: 5px; }
        .note-text { font-size: 14px; color: #666; line-height: 1.4; }
        
        .locked-item {
            opacity: 0.6;
            background: #f8f8f8;
            border-left-color: #ccc;
            display: none; /* 預設隱藏不符合的，讓畫面乾淨，也可改為 block */
        }
        .show-locked .locked-item { display: block; }

        /* === 底部資訊 === */
        .footer {
            margin-top: 30px;
            text-align: center;
            font-size: 13px;
            color: #888;
            padding: 20px;
            background: #f1f3f5;
        }
        .contact-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 15px;
            text-align: left;
        }
        .contact-title { font-weight: bold; color: var(--primary-color); margin-bottom: 5px; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <div class="header-box">
        <div class="header-title">⛰️ 復興區長者福利小幫手</div>
        <div class="header-subtitle">桃園市復興區長 <span class="mayor-name">蘇佐璽</span> 關心您 ❤️</div>
    </div>

    <div class="container">
        <div class="input-card">
            <div class="section-title">請勾選長輩狀況</div>
            
            <div class="form-group">
                <label>長輩年齡 (歲)</label>
                <div class="age-input-group">
                    <input type="number" id="age" value="55" min="50" max="120" oninput="calculate()">
                    <span style="font-size: 14px; color: #666;">(本系統以原住民身分試算)</span>
                </div>
            </div>

            <div class="checkbox-grid">
                <label class="checkbox-item"><input type="checkbox" id="is_farmer" onchange="calculate()"> 🌱 農保身分</label>
                <label class="checkbox-item"><input type="checkbox" id="is_low_income" onchange="calculate()"> 📉 中低收入</label>
                <label class="checkbox-item"><input type="checkbox" id="has_disability" onchange="calculate()"> ♿ 身障手冊</label>
                <label class="checkbox-item"><input type="checkbox" id="is_owner" onchange="calculate()"> 🏠 自有住宅</label>
                <label class="checkbox-item"><input type="checkbox" id="is_renter" onchange="calculate()"> 🔑 租賃房屋</label>
                <label class="checkbox-item"><input type="checkbox" id="grandparenting" onchange="calculate()"> 👶 照顧孫子女</label>
            </div>
        </div>

        <div class="section-title">💰 您的專屬福利試算結果</div>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('tab1', this)">💵 現金津貼</button>
            <button class="tab-btn" onclick="switchTab('tab2', this)">🩺 醫療照護</button>
            <button class="tab-btn" onclick="switchTab('tab3', this)">🏠 居住交通</button>
            <button class="tab-btn" onclick="switchTab('tab4', this)">🛡️ 其他權益</button>
        </div>

        <div id="tab1" class="benefit-list active">
            </div>
        <div id="tab2" class="benefit-list"></div>
        <div id="tab3" class="benefit-list"></div>
        <div id="tab4" class="benefit-list"></div>

        <div style="text-align: center; margin-top: 10px;">
            <label style="font-size: 14px; color: #666; cursor: pointer;">
                <input type="checkbox" id="show_all" onchange="toggleLocked()"> 顯示未符合項目
            </label>
        </div>
    </div>

    <div class="footer">
        <div class="container">
            <div class="contact-grid">
                <div>
                    <div class="contact-title">📞 服務專線</div>
                    <div>🔹 復興區公所：(03) 382-1500</div>
                    <div>🔹 市民專線：1999</div>
                </div>
                <div>
                    <div class="contact-title">🏥 照護資源</div>
                    <div>🔸 長照專線：1966</div>
                    <div>🔸 衛生所：(03) 382-2325</div>
                </div>
            </div>
            <div style="margin-top: 10px;">
                ⚠️ 本試算系統僅供參考，實際資格以政府機關最新核定為準。
            </div>
        </div>
    </div>

    <script>
        // 資料庫：所有福利項目邏輯
        const benefits = [
            // === Tab 1: 現金 ===
            { tab: 'tab1', name: "桃園老人三節禮金", money: "$2,500/每節 (年領$7,500)", note: "原住民55歲設籍滿6個月", unit: "區公所社會課", check: (d) => d.age >= 55 },
            { tab: 'tab1', name: "桃園重陽敬老金", money: "$2,500/年", note: "原住民55歲 (一般65歲)", unit: "區公所社會課", check: (d) => d.age >= 55 },
            { tab: 'tab1', name: "原住民給付 (國保)", money: "$4,049/月", note: "55-64歲專屬 (與老農互斥)", unit: "區公所原民課", check: (d) => d.age >= 55 && d.age < 65 && !d.is_farmer },
            { tab: 'tab1', name: "老農津貼", money: "$8,110/月", note: "農保年資滿15年", unit: "地區農會", check: (d) => d.is_farmer && d.age >= 65 },
            { tab: 'tab1', name: "桃園原民急難救助", money: "最高3萬", note: "意外/重病/死亡 (3個月內申請)", unit: "區公所原民課", check: (d) => true },
            { tab: 'tab1', name: "弱勢兒少托育(隔代)", money: "$3,000起/月", note: "祖父母照顧孫子女補助", unit: "區公所社會課", check: (d) => d.grandparenting && d.is_low_income },

            // === Tab 2: 醫療 ===
            { tab: 'tab2', name: "桃園原民假牙補助", money: "最高4.4萬", note: "需先至診所估價", unit: "區公所原民課", check: (d) => d.age >= 55 },
            { tab: 'tab2', name: "健保費全額補助", money: "全額減免", note: "55-64歲原住民 (系統自動減免)", unit: "健保局", check: (d) => d.age >= 55 },
            { tab: 'tab2', name: "成人健康檢查", money: "免費", note: "每年一次 (原住民提早至55歲)", unit: "衛生所", check: (d) => d.age >= 55 },
            { tab: 'tab2', name: "身障輔具補助", money: "全額/部分", note: "助聽器/氣墊床等", unit: "區公所社會課", check: (d) => d.has_disability },

            // === Tab 3: 居住交通 ===
            { tab: 'tab3', name: "復興區敬老愛心卡", money: "每月1000點", note: "復興區民專屬福利 (一般區800點)", unit: "區公所社會課", check: (d) => d.age >= 55, highlight: true },
            { tab: 'tab3', name: "愛心計程車", money: "點數折抵", note: "單趟100元以下補36點", unit: "各大車隊", check: (d) => d.age >= 55 },
            { tab: 'tab3', name: "桃園修繕住宅補助", money: "最高15萬", note: "屋頂/衛浴修繕 (需自有)", unit: "區公所原民課", check: (d) => d.is_owner },
            { tab: 'tab3', name: "桃園建購住宅補助", money: "最高22萬", note: "購買或自建房屋", unit: "區公所原民課", check: (d) => d.is_owner },
            { tab: 'tab3', name: "租金補貼 (300億)", money: "依等級 ($3000起)", note: "租屋者可申請", unit: "營建署", check: (d) => d.is_renter },

            // === Tab 4: 其他 ===
            { tab: 'tab4', name: "農保喪葬津貼", money: "$153,000", note: "農民身故 (由家屬請領)", unit: "農會保險部", check: (d) => d.is_farmer },
            { tab: 'tab4', name: "國保喪葬給付", money: "約9.8萬", note: "一般國保身故 (由家屬請領)", unit: "勞保局", check: (d) => !d.is_farmer },
            { tab: 'tab4', name: "原住民法律扶助", money: "律師費全免", note: "訴訟/法律諮詢", unit: "法扶基金會", check: (d) => true },
            { tab: 'tab4', name: "意外保險 (微型)", money: "最高30萬", note: "市府代為投保", unit: "社會局", check: (d) => d.is_low_income }
        ];

        function calculate() {
            // 1. 獲取當前輸入
            const data = {
                age: parseInt(document.getElementById('age').value) || 0,
                is_farmer: document.getElementById('is_farmer').checked,
                is_low_income: document.getElementById('is_low_income').checked,
                has_disability: document.getElementById('has_disability').checked,
                is_owner: document.getElementById('is_owner').checked,
                is_renter: document.getElementById('is_renter').checked,
                grandparenting: document.getElementById('grandparenting').checked
            };

            // 2. 清空顯示區
            ['tab1', 'tab2', 'tab3', 'tab4'].forEach(id => {
                document.getElementById(id).innerHTML = '';
            });

            // 3. 生成卡片
            benefits.forEach((item, index) => {
                const qualify = item.check(data);
                const container = document.getElementById(item.tab);
                
                // 決定樣式
                let className = "result-card";
                if (item.highlight && qualify) className += " highlight";
                if (!qualify) className += " locked-item";

                const html = `
                    <div class="${className}">
                        <div class="card-header">
                            <span class="benefit-name">${index + 1}. ${item.name}</span>
                            <span class="location-tag">${item.unit}</span>
                        </div>
                        ${qualify ? `<div class="money-text">${item.money}</div>` : ''}
                        <div class="note-text">
                            ${qualify ? '💡' : '🔒'} ${item.note} 
                            ${!qualify ? '(未符條件)' : ''}
                        </div>
                    </div>
                `;
                container.innerHTML += html;
            });
        }

        function switchTab(tabId, btn) {
            // 切換內容
            document.querySelectorAll('.benefit-list').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');

            // 切換按鈕樣式
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            btn.classList.add('active');
        }

        function toggleLocked() {
            const show = document.getElementById('show_all').checked;
            const container = document.querySelector('.container');
            if(show) container.classList.add('show-locked');
            else container.classList.remove('show-locked');
        }

        // 初始化
        calculate();
    </script>
</body>
</html>
