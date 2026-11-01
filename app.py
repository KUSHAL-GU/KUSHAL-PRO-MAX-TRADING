<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kushal Pro Max Trading - Indian Market</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { background-color: #0b0f19; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }
        .trading-card { background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(30, 41, 59, 0.8); backdrop-filter: blur(12px); transition: all 0.2s; }
        .trading-card:hover { border-color: #10b981; transform: translateY(-2px); }
        .glow-text { text-shadow: 0 0 10px rgba(16, 185, 129, 0.3); }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0b0f19; }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between p-4 md:p-6">
    <div>
        <header class="flex flex-col md:flex-row items-center justify-between border-b border-slate-800 pb-4 mb-6 gap-4">
            <div class="flex items-center gap-6">
                <a href="index.html" class="flex items-center gap-2 group text-left">
                    <div class="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20 group-hover:border-emerald-500/50 transition">
                        <i data-lucide="arrow-left" class="w-5 h-5 text-emerald-400"></i>
                    </div>
                    <div>
                        <span class="text-sm md:text-base font-bold tracking-wider text-emerald-400 glow-text block uppercase">Kushal Pro Max Trading</span>
                        <span class="text-[10px] text-slate-400 tracking-widest uppercase">Indian Market Terminal</span>
                    </div>
                </a>
            </div>
            <div class="flex items-center gap-3 w-full md:w-auto">
                <div class="relative w-full md:w-72">
                    <i data-lucide="search" class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"></i>
                    <input type="text" id="searchInput" onkeyup="filterCards()" placeholder="Search Nifty, Sensex, TCS..." 
                           class="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-4 py-2 text-xs text-slate-200 focus:outline-none focus:border-emerald-500">
                </div>
            </div>
        </header>

        <main>
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-xs uppercase font-bold tracking-wider text-slate-400">Indian Indices & Key Stocks</h2>
                <span class="text-[11px] text-slate-500">Click card for Performance Chart & Analytics</span>
            </div>
            <div id="cardsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>
        </main>
    </div>

    <!-- MODAL -->
    <div id="chartModal" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden items-center justify-center p-4 z-50">
        <div class="bg-slate-900 border border-slate-800 rounded-xl w-full max-w-5xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
            <div class="flex items-center justify-between p-4 border-b border-slate-800 bg-slate-950">
                <div class="flex items-center gap-3">
                    <h3 id="modalTitle" class="text-base font-bold text-slate-100"></h3>
                    <span id="modalPrice" class="text-sm font-semibold text-emerald-400"></span>
                    <span id="modalChange" class="text-xs font-medium"></span>
                </div>
                <div class="flex items-center gap-3">
                    <button id="chartSwitchBtn" onclick="toggleChartMode()" class="px-3 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-md text-xs font-semibold hover:bg-emerald-500/20 transition flex items-center gap-1.5">
                        <i data-lucide="candlestick-chart" class="w-4 h-4"></i><span>Switch to TradingView Candlestick</span>
                    </button>
                    <button onclick="closeModal()" class="text-slate-400 hover:text-white"><i data-lucide="x" class="w-5 h-5"></i></button>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto p-4 space-y-6">
                <div class="bg-slate-950/70 border border-slate-800 rounded-lg p-3 h-[380px] relative">
                    <div id="lineChartWrapper" class="w-full h-full"><canvas id="simpleLineChart"></canvas></div>
                    <div id="tradingviewWrapper" class="w-full h-full hidden"><div id="tradingview_widget_container" class="w-full h-full"></div></div>
                </div>
                <!-- Fundamentals -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-slate-950 border border-slate-800 rounded-lg p-4 text-xs space-y-2">
                        <h4 class="font-bold uppercase text-slate-400 mb-2">Market Metrics</h4>
                        <div class="flex justify-between"><span class="text-slate-500">Today Open:</span><strong id="mOpen" class="text-slate-200"></strong></div>
                        <div class="flex justify-between"><span class="text-slate-500">Prev Close:</span><strong id="mClose" class="text-slate-200"></strong></div>
                        <div class="flex justify-between"><span class="text-slate-500">52W High / Low:</span><strong id="mHighLow" class="text-slate-200"></strong></div>
                    </div>
                    <div class="bg-slate-950 border border-slate-800 rounded-lg p-4 text-xs space-y-2">
                        <h4 class="font-bold uppercase text-slate-400 mb-2">Shareholding Pattern</h4>
                        <div class="flex justify-between"><span class="text-slate-400">Promoter:</span><strong id="mPromoter" class="text-slate-200"></strong></div>
                        <div class="flex justify-between"><span class="text-slate-400">FII / DII:</span><strong id="mFii" class="text-slate-200"></strong></div>
                        <div class="flex justify-between"><span class="text-slate-400">Public:</span><strong id="mPublic" class="text-slate-200"></strong></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();
        const dataList = [
            { id: 'nifty', name: 'NIFTY 50', tv: 'NSE:NIFTY', price: 24350, change: 120, pct: 0.50, open: 24230, pClose: 24210, hl: '26,277 / 21,285', promoter: '71.77%', fii: '12.45%', pub: '15.78%' },
            { id: 'sensex', name: 'SENSEX', tv: 'BSE:SENSEX', price: 79800, change: 310, pct: 0.39, open: 79490, pClose: 79490, hl: '85,978 / 70,150', promoter: '70.50%', fii: '14.00%', pub: '15.50%' },
            { id: 'tcs', name: 'TCS (Tata Consultancy)', tv: 'NSE:TCS', price: 4150, change: 45, pct: 1.10, open: 4100, pClose: 4104, hl: '4,585 / 3,313', promoter: '71.77%', fii: '12.45%', pub: '15.78%' },
            { id: 'reliance', name: 'RELIANCE INDUSTRIES', tv: 'NSE:RELIANCE', price: 2980, change: -12, pct: -0.41, open: 2995, pClose: 2992, hl: '3,217 / 2,220', promoter: '50.30%', fii: '22.10%', pub: '27.60%' }
        ];

        function renderCards(list) {
            const grid = document.getElementById('cardsGrid');
            grid.innerHTML = '';
            list.forEach(i => {
                const pos = i.change >= 0;
                grid.innerHTML += `
                    <div onclick="openModal('${i.id}')" class="trading-card rounded-xl p-4 cursor-pointer space-y-3">
                        <div class="flex justify-between items-center"><span class="font-bold text-sm text-slate-100">${i.name}</span>
                        <span class="text-xs px-2 py-0.5 rounded ${pos ? 'text-emerald-400 bg-emerald-500/10' : 'text-rose-400 bg-rose-500/10'}">${pos ? '+' : ''}${i.pct}%</span></div>
                        <div class="text-2xl font-extrabold ${pos ? 'text-emerald-400' : 'text-rose-400'}">${i.price.toLocaleString()}</div>
                        <div class="text-xs text-slate-400">Open: ${i.open} | Prev Close: ${i.pClose}</div>
                    </div>`;
            });
        }
        renderCards(dataList);

        function filterCards() {
            const q = document.getElementById('searchInput').value.toLowerCase();
            renderCards(dataList.filter(i => i.name.toLowerCase().includes(q)));
        }

        let activeItem = null, mode = 'LINE', chartInst = null;
        function openModal(id) {
            activeItem = dataList.find(x => x.id === id);
            document.getElementById('modalTitle').innerText = activeItem.name;
            document.getElementById('modalPrice').innerText = activeItem.price.toLocaleString();
            document.getElementById('modalChange').innerText = `${activeItem.change >= 0 ? '+' : ''}${activeItem.change} (${activeItem.pct}%)`;
            document.getElementById('mOpen').innerText = activeItem.open;
            document.getElementById('mClose').innerText = activeItem.pClose;
            document.getElementById('mHighLow').innerText = activeItem.hl;
            document.getElementById('mPromoter').innerText = activeItem.promoter;
            document.getElementById('mFii').innerText = activeItem.fii;
            document.getElementById('mPublic').innerText = activeItem.pub;
            
            mode = 'LINE';
            updateChart();
            document.getElementById('chartModal').classList.remove('hidden');
            document.getElementById('chartModal').classList.add('flex');
        }

        function toggleChartMode() {
            mode = mode === 'LINE' ? 'CANDLE' : 'LINE';
            updateChart();
        }

        function updateChart() {
            if (mode === 'LINE') {
                document.getElementById('lineChartWrapper').classList.remove('hidden');
                document.getElementById('tradingviewWrapper').classList.add('hidden');
                document.getElementById('chartSwitchBtn').innerHTML = `<i data-lucide="candlestick-chart" class="w-4 h-4"></i><span>Switch to TradingView Candlestick</span>`;
                
                const ctx = document.getElementById('simpleLineChart').getContext('2d');
                if (chartInst) chartInst.destroy();
                chartInst = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['9:15', '10:00', '11:00', '12:00', '1:00', '2:00', '3:30'],
                        datasets: [{ data: [activeItem.open, activeItem.open+10, activeItem.open-20, activeItem.price-15, activeItem.price+5, activeItem.price], borderColor: '#10b981', fill: true, backgroundColor: 'rgba(16,185,129,0.1)', tension: 0.3 }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
                });
            } else {
                document.getElementById('lineChartWrapper').classList.add('hidden');
                document.getElementById('tradingviewWrapper').classList.remove('hidden');
                document.getElementById('chartSwitchBtn').innerHTML = `<i data-lucide="line-chart" class="w-4 h-4"></i><span>Switch to Simple Line Chart</span>`;
                document.getElementById('tradingview_widget_container').innerHTML = '';
                new TradingView.widget({ "autosize": true, "symbol": activeItem.tv, "interval": "5", "theme": "dark", "style": "1", "locale": "en", "container_id": "tradingview_widget_container" });
            }
            lucide.createIcons();
        }

        function closeModal() { document.getElementById('chartModal').classList.add('hidden'); }
    </script>
</body>
</html>
