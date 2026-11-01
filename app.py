<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kushal Pro Max Trading</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js for Simple Line Chart -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- TradingView Widget Script -->
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body {
            background-color: #0b0f19;
            color: #e2e8f0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .trading-card {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(12px);
            transition: all 0.2s ease-in-out;
        }
        .trading-card:hover {
            border-color: #10b981;
            transform: translateY(-2px);
        }
        .glow-text {
            text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
        }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0b0f19; }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between p-4 md:p-6">

    <!-- ========================================== -->
    <!-- STEP 1: SECURE LOGIN SCREEN                -->
    <!-- ========================================== -->
    <div id="loginScreen" class="fixed inset-0 bg-[#0b0f19] flex items-center justify-center p-4 z-50">
        <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl w-full max-w-md shadow-2xl space-y-6">
            <div class="text-center space-y-2">
                <div class="inline-block p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 mb-2">
                    <i data-lucide="shield-check" class="w-8 h-8 text-emerald-400"></i>
                </div>
                <h1 class="text-xl font-bold text-emerald-400 glow-text uppercase tracking-wider">Kushal Pro Max Trading</h1>
                <p class="text-xs text-slate-400">Enter your credentials to access secure terminal</p>
            </div>

            <form onsubmit="handleLogin(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-medium text-slate-400 mb-1">User ID / Username</label>
                    <input type="text" id="userId" required placeholder="Enter User ID" 
                           class="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500">
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-400 mb-1">Password</label>
                    <input type="password" id="password" required placeholder="••••••••" 
                           class="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500">
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-400 mb-1">6-Digit Secure PIN</label>
                    <input type="password" id="securePin" maxlength="6" required placeholder="••••••" 
                           class="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-xs text-slate-200 tracking-widest text-center focus:outline-none focus:border-emerald-500">
                </div>
                <button type="submit" class="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold rounded-lg text-xs tracking-wider uppercase transition shadow-lg shadow-emerald-600/20">
                    Secure Login
                </button>
            </form>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- STEP 2: MARKET SELECTION SCREEN            -->
    <!-- ========================================== -->
    <div id="marketSelectionScreen" class="fixed inset-0 bg-[#0b0f19] hidden items-center justify-center p-4 z-40">
        <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl w-full max-w-xl shadow-2xl space-y-6 text-center">
            <div>
                <h2 class="text-lg font-bold text-slate-100 uppercase tracking-wide">Select Trading Market</h2>
                <p class="text-xs text-slate-400 mt-1">Choose your desired financial segment to open analytics terminal</p>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <!-- Indian Market (Active) -->
                <button onclick="selectMarket('INDIAN')" class="p-5 bg-emerald-500/10 border border-emerald-500/40 hover:border-emerald-500 rounded-xl flex flex-col items-center justify-center space-y-3 transition group">
                    <i data-lucide="trending-up" class="w-8 h-8 text-emerald-400 group-hover:scale-110 transition"></i>
                    <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Indian Market</span>
                </button>
                <!-- Crypto Market -->
                <button onclick="selectMarket('CRYPTO')" class="p-5 bg-slate-950 border border-slate-800 hover:border-slate-600 rounded-xl flex flex-col items-center justify-center space-y-3 transition group">
                    <i data-lucide="coins" class="w-8 h-8 text-slate-400 group-hover:scale-110 transition"></i>
                    <span class="text-xs font-bold text-slate-300 uppercase tracking-wider">Crypto Market</span>
                </button>
                <!-- US Market -->
                <button onclick="selectMarket('US')" class="p-5 bg-slate-950 border border-slate-800 hover:border-slate-600 rounded-xl flex flex-col items-center justify-center space-y-3 transition group">
                    <i data-lucide="globe" class="w-8 h-8 text-slate-400 group-hover:scale-110 transition"></i>
                    <span class="text-xs font-bold text-slate-300 uppercase tracking-wider">US Market</span>
                </button>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- STEP 3: MAIN INDIAN MARKET TERMINAL        -->
    <!-- ========================================== -->
    <div id="mainTerminal" class="hidden flex-col min-h-screen justify-between">
        <div>
            <!-- TOP HEADER -->
            <header class="flex flex-col md:flex-row items-center justify-between border-b border-slate-800 pb-4 mb-6 gap-4">
                <div class="flex items-center gap-6">
                    <!-- Clickable Brand Logo Button -->
                    <button onclick="returnToMarketSelection()" class="flex items-center gap-2 group text-left">
                        <div class="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20 group-hover:border-emerald-500/50 transition">
                            <i data-lucide="candlestick-chart" class="w-6 h-6 text-emerald-400"></i>
                        </div>
                        <div>
                            <span class="text-sm md:text-base font-bold tracking-wider text-emerald-400 glow-text block uppercase">Kushal Pro Max Trading</span>
                            <span class="text-[10px] text-slate-400 tracking-widest uppercase">Indian Market Terminal</span>
                        </div>
                    </button>

                    <!-- PREVIOUS SESSION METRICS -->
                    <div class="hidden lg:flex items-center gap-3 bg-slate-900/80 border border-slate-800 px-3 py-1.5 rounded-md text-xs">
                        <span class="text-slate-400 font-medium border-r border-slate-700 pr-2">Prev Session (30 Oct 2026)</span>
                        <span class="text-slate-300">Open: <strong class="text-slate-100">24,150.00</strong></span>
                        <span class="text-slate-500">|</span>
                        <span class="text-slate-300">Close: <strong class="text-slate-100">24,210.00</strong></span>
                    </div>
                </div>

                <!-- SEARCH & TOGGLE -->
                <div class="flex items-center gap-3 w-full md:w-auto">
                    <div class="relative w-full md:w-72">
                        <i data-lucide="search" class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"></i>
                        <input type="text" id="searchInput" onkeyup="filterCards()" placeholder="Search Index, Stock (TCS, Reliance)..." 
                               class="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition">
                    </div>
                    <button id="marketToggleBtn" onclick="toggleMarketStatus()" class="px-3 py-2 rounded-lg border border-slate-700 text-xs font-semibold flex items-center gap-1.5 whitespace-nowrap bg-slate-900 text-emerald-400">
                        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                        <span>Live Market</span>
                    </button>
                </div>
            </header>

            <!-- MARKET CARDS GRID -->
            <main>
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-xs uppercase font-bold tracking-wider text-slate-400">Major Indian Indices & Constituents</h2>
                    <span class="text-[11px] text-slate-500">Click any card to open detailed performance chart</span>
                </div>

                <div id="cardsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <!-- Cards will load here -->
                </div>
            </main>
        </div>

        <!-- FOOTER -->
        <footer class="mt-8 border-t border-slate-800/80 pt-4 flex flex-col sm:flex-row items-center justify-between text-[11px] text-slate-500 gap-2">
            <div>Kushal Pro Max Trading Platform &copy; 2026. All rights reserved.</div>
            <div class="flex items-center gap-4">
                <span>NSE/BSE Data Stream: <strong class="text-emerald-400">Connected</strong></span>
                <span>Latency: <strong class="text-slate-300">12ms</strong></span>
            </div>
        </footer>
    </div>

    <!-- ========================================== -->
    <!-- DETAILED CHART & FUNDAMENTALS MODAL        -->
    <!-- ========================================== -->
    <div id="chartModal" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden items-center justify-center p-4 z-50">
        <div class="bg-slate-900 border border-slate-800 rounded-xl w-full max-w-5xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
            
            <div class="flex items-center justify-between p-4 border-b border-slate-800 bg-slate-950">
                <div class="flex items-center gap-3">
                    <h3 id="modalTitle" class="text-base font-bold text-slate-100">NIFTY 50</h3>
                    <span id="modalPrice" class="text-sm font-semibold text-emerald-400">24,350.50</span>
                    <span id="modalChange" class="text-xs text-emerald-400 font-medium">+120.30 (+0.50%)</span>
                </div>
                
                <div class="flex items-center gap-3">
                    <button id="chartSwitchBtn" onclick="toggleChartMode()" class="px-3 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-md text-xs font-semibold hover:bg-emerald-500/20 transition flex items-center gap-1.5">
                        <i data-lucide="candlestick-chart" class="w-4 h-4"></i>
                        <span>Switch to TradingView Candlestick</span>
                    </button>
                    <button onclick="closeModal()" class="text-slate-400 hover:text-white p-1">
                        <i data-lucide="x" class="w-5 h-5"></i>
                    </button>
                </div>
            </div>

            <div class="flex-1 overflow-y-auto p-4 space-y-6">
                <!-- CHART CONTAINER -->
                <div class="bg-slate-950/70 border border-slate-800 rounded-lg p-3 h-[380px] relative">
                    <div id="lineChartWrapper" class="w-full h-full">
                        <canvas id="simpleLineChart"></canvas>
                    </div>
                    <div id="tradingviewWrapper" class="w-full h-full hidden">
                        <div id="tradingview_widget_container" class="w-full h-full"></div>
                    </div>
                </div>

                <!-- FUNDAMENTALS SECTION -->
                <div id="fundamentalsSection" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-slate-950 border border-slate-800 rounded-lg p-4">
                        <h4 class="text-xs font-bold uppercase text-slate-400 mb-3 flex items-center gap-1.5">
                            <i data-lucide="activity" class="w-4 h-4 text-emerald-400"></i> Market Trading Metrics
                        </h4>
                        <div class="grid grid-cols-2 gap-3 text-xs">
                            <div><span class="text-slate-500 block">Today Open</span><span id="metricTodayOpen" class="font-semibold text-slate-200"></span></div>
                            <div><span class="text-slate-500 block">Previous Close</span><span id="metricPrevClose" class="font-semibold text-slate-200"></span></div>
                            <div><span class="text-slate-500 block">52-Week High</span><span id="metric52High" class="font-semibold text-slate-200"></span></div>
                            <div><span class="text-slate-500 block">52-Week Low</span><span id="metric52Low" class="font-semibold text-slate-200"></span></div>
                            <div><span class="text-slate-500 block">Total Volume</span><span id="metricVolume" class="font-semibold text-slate-200"></span></div>
                            <div><span class="text-slate-500 block">Market Cap</span><span id="metricMarketCap" class="font-semibold text-slate-200"></span></div>
                        </div>
                    </div>

                    <div class="bg-slate-950 border border-slate-800 rounded-lg p-4">
                        <h4 class="text-xs font-bold uppercase text-slate-400 mb-3 flex items-center gap-1.5">
                            <i data-lucide="pie-chart" class="w-4 h-4 text-emerald-400"></i> Shareholding Pattern
                        </h4>
                        <div class="space-y-2.5 text-xs">
                            <div>
                                <div class="flex justify-between mb-1"><span class="text-slate-400">Promoter Holding</span><span id="promoterVal" class="font-bold text-slate-200"></span></div>
                                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden"><div id="promoterBar" class="bg-emerald-500 h-full"></div></div>
                            </div>
                            <div>
                                <div class="flex justify-between mb-1"><span class="text-slate-400">FII (Foreign Institutional)</span><span id="fiiVal" class="font-bold text-slate-200"></span></div>
                                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden"><div id="fiiBar" class="bg-blue-500 h-full"></div></div>
                            </div>
                            <div>
                                <div class="flex justify-between mb-1"><span class="text-slate-400">DII (Domestic Mutual Funds)</span><span id="diiVal" class="font-bold text-slate-200"></span></div>
                                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden"><div id="diiBar" class="bg-purple-500 h-full"></div></div>
                            </div>
                            <div>
                                <div class="flex justify-between mb-1"><span class="text-slate-400">Public & Retail</span><span id="publicVal" class="font-bold text-slate-200"></span></div>
                                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden"><div id="publicBar" class="bg-amber-500 h-full"></div></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- JAVASCRIPT LOGIC & ROUTING                 -->
    <!-- ========================================== -->
    <script>
        lucide.createIcons();

        // 1. AUTH & FLOW NAVIGATION
        function handleLogin(e) {
            e.preventDefault();
            const pin = document.getElementById('securePin').value;
            if (pin.length !== 6) {
                alert('Please enter a valid 6-digit secure PIN.');
                return;
            }
            // Transition from Login to Market Selection
            document.getElementById('loginScreen').classList.add('hidden');
            document.getElementById('marketSelectionScreen').classList.remove('hidden');
            document.getElementById('marketSelectionScreen').classList.add('flex');
        }

        function selectMarket(marketType) {
            if (marketType === 'INDIAN') {
                // Transition from Market Selection to Indian Market Terminal
                document.getElementById('marketSelectionScreen').classList.add('hidden');
                document.getElementById('marketSelectionScreen').classList.remove('flex');
                
                const terminal = document.getElementById('mainTerminal');
                terminal.classList.remove('hidden');
                terminal.classList.add('flex');
                renderCards(indicesData);
            } else {
                alert(marketType + ' Market module is under development. Opening Indian Market instead.');
                selectMarket('INDIAN');
            }
        }

        function returnToMarketSelection() {
            document.getElementById('mainTerminal').classList.add('hidden');
            document.getElementById('mainTerminal').classList.remove('flex');
            
            const marketSel = document.getElementById('marketSelectionScreen');
            marketSel.classList.remove('hidden');
            marketSel.classList.add('flex');
        }

        // 2. DATA LIST
        let isMarketLive = true;
        let activeChartMode = 'LINE';
        let currentActiveItem = null;
        let lineChartInstance = null;

        const indicesData = [
            { id: 'nifty50', name: 'NIFTY 50', tvSymbol: 'NSE:NIFTY', price: 24350.50, change: 120.30, percent: 0.50, open: 24230.00, prevDate: '30 Oct 2026', prevOpen: 24150.00, prevClose: 24210.00, promoter: '71.77%', fii: '12.45%', dii: '10.30%', public: '5.48%', cap: '₹15.4T', vol: '14.2M', h52: '26,277.35', l52: '21,285.55' },
            { id: 'banknifty', name: 'BANK NIFTY', tvSymbol: 'NSE:BANKNIFTY', price: 52100.20, change: -180.50, percent: -0.35, open: 52280.00, prevDate: '30 Oct 2026', prevOpen: 52400.00, prevClose: 52280.00, promoter: '68.20%', fii: '15.10%', dii: '11.40%', public: '5.30%', cap: '₹12.1T', vol: '18.5M', h52: '54,467.30', l52: '44,420.00' },
            { id: 'sensex', name: 'SENSEX', tvSymbol: 'BSE:SENSEX', price: 79800.10, change: 310.00, percent: 0.39, open: 79490.00, prevDate: '30 Oct 2026', prevOpen: 79200.00, prevClose: 79490.00, promoter: '70.50%', fii: '14.00%', dii: '10.80%', public: '4.70%', cap: '₹18.2T', vol: '8.4M', h52: '85,978.25', l52: '70,150.00' },
            { id: 'next50', name: 'NIFTY NEXT 50', tvSymbol: 'NSE:NIFTYJR', price: 71250.80, change: 240.10, percent: 0.34, open: 71010.00, prevDate: '30 Oct 2026', prevOpen: 70800.00, prevClose: 71010.00, promoter: '65.00%', fii: '18.20%', dii: '12.10%', public: '4.70%', cap: '₹8.4T', vol: '6.1M', h52: '76,500.00', l52: '60,100.00' },
            { id: 'midcap', name: 'NIFTY MIDCAP 100', tvSymbol: 'NSE:NIFTY_MIDCAP_100', price: 58400.00, change: -95.40, percent: -0.16, open: 58550.00, prevDate: '30 Oct 2026', prevOpen: 58700.00, prevClose: 58495.40, promoter: '58.40%', fii: '20.10%', dii: '14.50%', public: '7.00%', cap: '₹6.2T', vol: '22.8M', h52: '60,150.00', l52: '45,200.00' },
            { id: 'smallcap', name: 'NIFTY SMALLCAP 100', tvSymbol: 'NSE:NIFTY_SMALLCAP_100', price: 18920.40, change: 115.60, percent: 0.61, open: 18800.00, prevDate: '30 Oct 2026', prevOpen: 18700.00, prevClose: 18804.80, promoter: '52.10%', fii: '22.40%', dii: '15.20%', public: '10.30%', cap: '₹3.8T', vol: '35.4M', h52: '19,500.00', l52: '13,800.00' },
            { id: 'tcs', name: 'TCS (Tata Consultancy)', tvSymbol: 'NSE:TCS', price: 4150.00, change: 45.20, percent: 1.10, open: 4100.00, prevDate: '30 Oct 2026', prevOpen: 4080.00, prevClose: 4104.80, promoter: '71.77%', fii: '12.45%', dii: '10.30%', public: '5.48%', cap: '₹15.0T', vol: '2.1M', h52: '4,585.90', l52: '3,313.00' },
            { id: 'reliance', name: 'RELIANCE INDUSTRIES', tvSymbol: 'NSE:RELIANCE', price: 2980.50, change: -12.30, percent: -0.41, open: 2995.00, prevDate: '30 Oct 2026', prevOpen: 3010.00, prevClose: 2992.80, promoter: '50.30%', fii: '22.10%', dii: '16.40%', public: '11.20%', cap: '₹20.1T', vol: '5.6M', h52: '3,217.90', l52: '2,220.30' }
        ];

        // 3. RENDER CARDS
        function renderCards(dataList) {
            const grid = document.getElementById('cardsGrid');
            grid.innerHTML = '';

            dataList.forEach(item => {
                const isPositive = item.change >= 0;
                const colorClass = isPositive ? 'text-emerald-400' : 'text-rose-400';
                const bgTag = isPositive ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-rose-500/10 border-rose-500/30';
                const arrow = isPositive ? '▲' : '▼';

                const cardHtml = `
                    <div onclick="openChartModal('${item.id}')" class="trading-card rounded-xl p-4 cursor-pointer flex flex-col justify-between space-y-4">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-sm tracking-wide text-slate-100">${item.name}</span>
                            <span class="text-[10px] font-bold px-2 py-0.5 rounded border ${bgTag} ${colorClass}">
                                ${arrow} ${isPositive ? '+' : ''}${item.percent}%
                            </span>
                        </div>
                        <div>
                            <div class="text-2xl font-extrabold ${colorClass} tracking-tight">
                                ${item.price.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                            </div>
                            <div class="text-xs text-slate-400 mt-1">
                                Today Open: <strong class="text-slate-200">${item.open.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</strong>
                            </div>
                        </div>
                        <div class="border-t border-slate-800 pt-2 text-[11px] text-slate-400 flex items-center justify-between">
                            <span>Prev (${item.prevDate}):</span>
                            <span>Open: <strong class="text-slate-300">${item.prevOpen}</strong> | Close: <strong class="text-slate-300">${item.prevClose}</strong></span>
                        </div>
                    </div>
                `;
                grid.innerHTML += cardHtml;
            });
        }

        // 4. SEARCH FILTER
        function filterCards() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const filtered = indicesData.filter(item => 
                item.name.toLowerCase().includes(query) || 
                item.tvSymbol.toLowerCase().includes(query)
            );
            renderCards(filtered);
        }

        // 5. TOGGLE MARKET STATUS
        function toggleMarketStatus() {
            isMarketLive = !isMarketLive;
            const btn = document.getElementById('marketToggleBtn');
            if (isMarketLive) {
                btn.className = "px-3 py-2 rounded-lg border border-slate-700 text-xs font-semibold flex items-center gap-1.5 whitespace-nowrap bg-slate-900 text-emerald-400";
                btn.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span><span>Live Market</span>`;
            } else {
                btn.className = "px-3 py-2 rounded-lg border border-slate-700 text-xs font-semibold flex items-center gap-1.5 whitespace-nowrap bg-slate-900 text-rose-400";
                btn.innerHTML = `<span class="w-2 h-2 rounded-full bg-rose-500"></span><span>Market Closed</span>`;
            }
        }

        // 6. OPEN MODAL & CHARTS
        function openChartModal(itemId) {
            currentActiveItem = indicesData.find(i => i.id === itemId);
            if (!currentActiveItem) return;

            document.getElementById('modalTitle').innerText = currentActiveItem.name;
            document.getElementById('modalPrice').innerText = currentActiveItem.price.toLocaleString('en-IN', { minimumFractionDigits: 2 });
            document.getElementById('modalChange').innerText = `${currentActiveItem.change >= 0 ? '+' : ''}${currentActiveItem.change} (${currentActiveItem.percent}%)`;
            
            const isPos = currentActiveItem.change >= 0;
            document.getElementById('modalPrice').className = `text-sm font-semibold ${isPos ? 'text-emerald-400' : 'text-rose-400'}`;
            document.getElementById('modalChange').className = `text-xs font-medium ${isPos ? 'text-emerald-400' : 'text-rose-400'}`;

            document.getElementById('metricTodayOpen').innerText = currentActiveItem.open.toLocaleString();
            document.getElementById('metricPrevClose').innerText = currentActiveItem.prevClose.toLocaleString();
            document.getElementById('metric52High').innerText = currentActiveItem.h52;
            document.getElementById('metric52Low').innerText = currentActiveItem.l52;
            document.getElementById('metricVolume').innerText = currentActiveItem.vol;
            document.getElementById('metricMarketCap').innerText = currentActiveItem.cap;

            document.getElementById('promoterVal').innerText = currentActiveItem.promoter;
            document.getElementById('promoterBar').style.width = currentActiveItem.promoter;
            document.getElementById('fiiVal').innerText = currentActiveItem.fii;
            document.getElementById('fiiBar').style.width = currentActiveItem.fii;
            document.getElementById('diiVal').innerText = currentActiveItem.dii;
            document.getElementById('diiBar').style.width = currentActiveItem.dii;
            document.getElementById('publicVal').innerText = currentActiveItem.public;
            document.getElementById('publicBar').style.width = currentActiveItem.public;

            activeChartMode = 'LINE';
            updateChartDisplay();

            document.getElementById('chartModal').classList.remove('hidden');
            document.getElementById('chartModal').classList.add('flex');
        }

        function toggleChartMode() {
            activeChartMode = activeChartMode === 'LINE' ? 'CANDLESTICK' : 'LINE';
            updateChartDisplay();
        }

        function updateChartDisplay() {
            const lineWrapper = document.getElementById('lineChartWrapper');
            const tvWrapper = document.getElementById('tradingviewWrapper');
            const btn = document.getElementById('chartSwitchBtn');

            if (activeChartMode === 'LINE') {
                lineWrapper.classList.remove('hidden');
                tvWrapper.classList.add('hidden');
                btn.innerHTML = `<i data-lucide="candlestick-chart" class="w-4 h-4"></i><span>Switch to TradingView Candlestick</span>`;
                renderLineChart(currentActiveItem);
            } else {
                lineWrapper.classList.add('hidden');
                tvWrapper.classList.remove('hidden');
                btn.innerHTML = `<i data-lucide="line-chart" class="w-4 h-4"></i><span>Switch to Simple Line Chart</span>`;
                renderTradingViewWidget(currentActiveItem.tvSymbol);
            }
            lucide.createIcons();
        }

        function renderLineChart(item) {
            const ctx = document.getElementById('simpleLineChart').getContext('2d');
            if (lineChartInstance) lineChartInstance.destroy();

            const isPositive = item.change >= 0;
            const lineColor = isPositive ? '#10b981' : '#f43f5e';
            const bgGradient = ctx.createLinearGradient(0, 0, 0, 300);
            bgGradient.addColorStop(0, isPositive ? 'rgba(16, 185, 129, 0.25)' : 'rgba(244, 63, 94, 0.25)');
            bgGradient.addColorStop(1, 'rgba(11, 15, 25, 0)');

            const basePrice = item.open;
            const dataPoints = [basePrice];
            for (let i = 1; i <= 20; i++) {
                const rand = (Math.random() - 0.48) * (basePrice * 0.005);
                dataPoints.push(dataPoints[i - 1] + rand);
            }
            dataPoints[dataPoints.length - 1] = item.price;

            lineChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Array.from({length: 21}, (_, i) => `9:${15 + i*15} AM`),
                    datasets: [{
                        label: item.name,
                        data: dataPoints,
                        borderColor: lineColor,
                        borderWidth: 2,
                        fill: true,
                        backgroundColor: bgGradient,
                        tension: 0.3,
                        pointRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: 'rgba(30, 41, 59, 0.5)' }, ticks: { color: '#64748b', font: { size: 10 } } },
                        y: { grid: { color: 'rgba(30, 41, 59, 0.5)' }, ticks: { color: '#64748b', font: { size: 10 } } }
                    }
                }
            });
        }

        function renderTradingViewWidget(symbol) {
            document.getElementById('tradingview_widget_container').innerHTML = '';
            new TradingView.widget({
                "autosize": true,
                "symbol": symbol,
                "interval": "5",
                "timezone": "Asia/Kolkata",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "#0f172a",
                "enable_publishing": false,
                "allow_symbol_change": true,
                "container_id": "tradingview_widget_container"
            });
        }

        function closeModal() {
            document.getElementById('chartModal').classList.add('hidden');
            document.getElementById('chartModal').classList.remove('flex');
        }
    </script>
</body>
</html>
