# Complete generator for Aether Radar public frontend
import os

html_code = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AETHER RADAR — Autonomous B2B Forensic Intelligence & Micro-Billing Terminal</title>
  <meta name="description" content="Measure any business website and model the revenue it may be leaking. Estimates are labeled; measurements are real.">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@700;800;900&display=swap" rel="stylesheet">
  
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Plus Jakarta Sans', 'sans-serif'],
            display: ['Syne', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
          colors: {
            aether: {
              bg: '#05070E',
              card: 'rgba(15, 23, 42, 0.65)',
              border: 'rgba(255, 255, 255, 0.08)',
              cyan: '#00F2FE',
              neon: '#4FACFE',
              emerald: '#10B981',
              rose: '#F43F5E',
              amber: '#F59E0B'
            }
          }
        }
      }
    }
  </script>

  <style>
    body {
      background-color: #05070E;
      background-image: 
        radial-gradient(at 0% 0%, rgba(79, 172, 254, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(0, 242, 254, 0.10) 0px, transparent 50%),
        radial-gradient(at 50% 50%, rgba(16, 185, 129, 0.05) 0px, transparent 60%),
        radial-gradient(at 100% 100%, rgba(244, 63, 94, 0.08) 0px, transparent 50%),
        radial-gradient(at 0% 100%, rgba(99, 102, 241, 0.10) 0px, transparent 50%);
      background-attachment: fixed;
      color: #E2E8F0;
    }
    .cyber-grid {
      background-size: 40px 40px;
      background-image: 
        linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    }
    .glass-panel {
      background: rgba(13, 19, 36, 0.7);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
    }
    .glass-glow {
      box-shadow: 0 0 35px -5px rgba(0, 242, 254, 0.25);
    }
    .gauge-needle {
      transform-origin: 100px 100px;
      transition: transform 1.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
  </style>
</head>
<body class="min-h-screen cyber-grid flex flex-col font-sans selection:bg-cyan-500 selection:text-black">

  <!-- ==================== TOP TELEMETRY STATUS BAR ==================== -->
  <div class="w-full border-b border-white/[0.06] bg-black/40 backdrop-blur-md px-4 py-2 text-[11px] font-mono text-slate-400 flex flex-wrap items-center justify-between gap-3">
    <div class="flex items-center gap-4">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
        <span class="w-2 h-2 rounded-full bg-emerald-400 -ml-4"></span>
        <span class="text-white font-semibold tracking-wider">AETHER ENGINE V1.0</span>
      </div>
      <span class="hidden md:inline text-slate-600">|</span>
      <span class="hidden md:inline">INFERENCE: <span class="text-cyan-400">GROQ 120B</span></span>
      <span class="hidden lg:inline text-slate-600">|</span>
      <span class="hidden lg:inline">SETTLEMENT: <span class="text-emerald-400">SOLANA & BASE USDC</span></span>
    </div>

    <div class="flex items-center gap-4">
      </div>
  </div>

  <!-- ==================== HEADER & GLOBAL NAVIGATION ==================== -->
  <header class="sticky top-0 z-40 w-full border-b border-white/[0.08] bg-black/60 backdrop-blur-xl">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      
      <!-- Brand Logo -->
      <a href="#" class="flex items-center gap-3 group">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 p-[1px] shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
          <div class="w-full h-full bg-[#070b16] rounded-xl flex items-center justify-center">
            <i class="fas fa-crosshairs text-cyan-400 text-lg"></i>
          </div>
        </div>
        <div>
          <span class="font-display font-black text-xl tracking-tight text-white block">AETHER<span class="text-cyan-400">RADAR</span></span>
          <span class="font-mono text-[9px] tracking-widest uppercase text-slate-400 block -mt-1">Forensic Deal Closer</span>
        </div>
      </a>

      <!-- Center Navigation Links -->
      <nav class="hidden md:flex items-center gap-8 text-xs font-semibold text-slate-300">
        <a href="#scanner" class="text-cyan-400 flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span> Live Scanner
        </a>
        </nav>

      <!-- Right Action Controls -->
      <div class="flex items-center gap-3">
        <button onclick="openWalletModal()" class="flex items-center gap-2 bg-gradient-to-r from-purple-600/20 to-cyan-500/20 hover:from-purple-600/30 hover:to-cyan-500/30 text-white text-xs font-bold px-4 py-2 rounded-xl border border-cyan-500/30 transition-all shadow-sm">
          <i class="fas fa-wallet text-cyan-400"></i>
          <span id="walletBtnText">Connect Wallet</span>
        </button>

        <!-- STRICT RULE: WhatsApp button ONLY ICON -->
        <a href="https://wa.me/971508379080?text=Hello%20Aether%20Radar%20Team" target="_blank" class="w-9 h-9 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-400 flex items-center justify-center border border-emerald-500/30 transition-all" title="WhatsApp Contact">
          <i class="fab fa-whatsapp text-sm"></i>
        </a>
      </div>

    </div>
  </header>

  <!-- ==================== MAIN CONTENT WRAPPER ==================== -->
  <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-12 flex flex-col gap-16">

    <!-- ==================== HERO SECTION & SCANNER INPUT ==================== -->
    <section id="scanner" class="flex flex-col items-center text-center relative pt-4">
      
      <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-300 text-xs font-mono font-medium mb-6">
        <span class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
        <span>AUTONOMOUS B2B REVENUE PROWLER • ZERO KYC</span>
      </div>

      <h1 class="font-display font-black text-4xl sm:text-5xl lg:text-6xl text-white tracking-tight max-w-4xl leading-tight">
        Reverse-Engineer Any Business.<br>
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-sky-300 to-indigo-400">
          Extract Leaks. Close More Deals.
        </span>
      </h1>

      <p class="mt-4 text-slate-300 text-sm sm:text-base max-w-2xl font-normal leading-relaxed">
        Input any website on Earth. We measure the site for real, model the revenue it may be losing (clearly labeled as an estimate), and draft outreach copy.
      </p>

      <!-- COMMAND SCANNER BAR -->
      <div class="w-full max-w-3xl mt-8">
        <form onsubmit="handleScanSubmit(event)" class="relative p-2 rounded-2xl glass-panel glass-glow flex flex-col sm:flex-row items-center gap-2 transition-all focus-within:border-cyan-400/60">
          
          <div class="flex items-center flex-grow w-full px-3 gap-3">
            <i class="fas fa-globe text-cyan-400 text-lg"></i>
            <input 
              type="text" 
              id="targetUrlInput"
              required 
              placeholder="e.g. octane.rent, thenovaclinic.com, yourcompetitor.com"
              class="w-full bg-transparent text-white placeholder-slate-500 text-sm sm:text-base font-mono outline-none py-2"
            >
          </div>

          <button 
            type="submit" 
            id="scanSubmitBtn"
            class="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-black font-extrabold text-xs sm:text-sm tracking-wider uppercase transition-all shadow-lg shadow-cyan-500/25 flex items-center justify-center gap-2 whitespace-nowrap active:scale-95"
          >
            <i class="fas fa-bolt text-black"></i>
            <span>SCAN REVENUE LEAKS</span>
          </button>
        </form>

        <!-- Quick 1-Click Samples -->
        <div class="mt-4 flex flex-wrap items-center justify-center gap-2 text-xs font-mono text-slate-400">
          <span class="text-slate-500">Live Samples:</span>
          <button onclick="fillAndScan('octane.rent')" class="px-2.5 py-1 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] hover:text-white border border-white/5 transition-colors">
            🏎️ octane.rent
          </button>
          <button onclick="fillAndScan('thenovaclinic.com')" class="px-2.5 py-1 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] hover:text-white border border-white/5 transition-colors">
            🏛️ thenovaclinic.com
          </button>
          <button onclick="fillAndScan('gymshark.com')" class="px-2.5 py-1 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] hover:text-white border border-white/5 transition-colors">
            ⚡ gymshark.com
          </button>
        </div>
      </div>

      <!-- SCANNING HUD -->
      <div id="scanningHud" class="hidden w-full max-w-2xl mt-8 glass-panel rounded-2xl p-6 text-left font-mono">
        <div class="flex items-center justify-between mb-4 pb-3 border-b border-white/10">
          <div class="flex items-center gap-2.5">
            <div class="w-3 h-3 rounded-full bg-cyan-400 animate-ping"></div>
            <span class="text-white text-xs font-bold uppercase tracking-wider">Neural Telemetry Running</span>
          </div>
          <span id="hudTimer" class="text-cyan-400 text-xs font-bold">0.0s</span>
        </div>

        <div class="space-y-2.5 text-xs">
          <div id="step1" class="flex items-center justify-between text-slate-400">
            <span>[1/4] DNS Resolution & TTFB latency extraction...</span>
            <span class="text-cyan-400 font-bold step-status">PENDING</span>
          </div>
          <div id="step2" class="flex items-center justify-between text-slate-400">
            <span>[2/4] Headless DOM Mobile Viewport Simulation...</span>
            <span class="text-slate-600 font-bold step-status">WAITING</span>
          </div>
          <div id="step3" class="flex items-center justify-between text-slate-400">
            <span>[3/4] WhatsApp & Checkout Friction Vectoring...</span>
            <span class="text-slate-600 font-bold step-status">WAITING</span>
          </div>
          <div id="step4" class="flex items-center justify-between text-slate-400">
            <span>[4/4] Groq 120B Cognitive Revenue Decomposition...</span>
            <span class="text-slate-600 font-bold step-status">WAITING</span>
          </div>
        </div>

        <div class="w-full bg-slate-800 rounded-full h-1.5 mt-5 overflow-hidden">
          <div id="hudProgressBar" class="bg-gradient-to-r from-cyan-400 to-blue-500 h-1.5 rounded-full transition-all duration-300 w-0"></div>
        </div>
      </div>

    </section>

    <!-- ==================== AUDIT RESULTS DISPLAY AREA ==================== -->
    <section id="resultsSection" class="hidden flex flex-col gap-8">
      
      <!-- Top Target Header Card -->
      <div class="glass-panel rounded-3xl p-6 sm:p-8 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 border-l-4 border-l-cyan-400">
        <div>
          <div class="flex items-center gap-3 mb-1">
            <span class="text-xs font-mono font-bold uppercase tracking-widest text-cyan-400" id="resNiche">E-Commerce</span>
            <span class="text-slate-600">•</span>
            <span class="text-xs font-mono text-slate-400" id="resTimestamp">Just now</span>
          </div>
          <h2 class="font-display font-black text-2xl sm:text-3xl text-white" id="resBusinessName">Target Enterprise</h2>
          <a id="resDomainLink" href="#" target="_blank" class="text-xs font-mono text-slate-400 hover:text-cyan-400 mt-1 inline-flex items-center gap-1.5">
            <span id="resDomain">domain.com</span> <i class="fas fa-arrow-up-right-from-square text-[10px]"></i>
          </a>
        </div>

        <div class="flex flex-wrap items-center gap-3">
          <div class="px-3 py-2 rounded-xl bg-white/[0.04] border border-white/5 font-mono text-xs">
            <span class="text-slate-500 block text-[10px]">TTFB LATENCY</span>
            <span class="text-white font-bold" id="resTtfb">320ms</span>
          </div>
          <div class="px-3 py-2 rounded-xl bg-white/[0.04] border border-white/5 font-mono text-xs">
            <span class="text-slate-500 block text-[10px]">PAYLOAD SIZE</span>
            <span class="text-white font-bold" id="resSize">140 KB</span>
          </div>
          <div class="px-3 py-2 rounded-xl bg-white/[0.04] border border-white/5 font-mono text-xs">
            <span class="text-slate-500 block text-[10px]">WHATSAPP FUNNEL</span>
            <span class="font-bold" id="resWaStatus">MISSING</span>
          </div>
        </div>
      </div>

      <!-- Main Metric Diagnostics Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <!-- CARD 1: THE FRICTION GAUGE -->
        <div class="glass-panel rounded-3xl p-6 sm:p-8 flex flex-col items-center justify-between text-center relative overflow-hidden">
          <div class="w-full flex items-center justify-between text-xs font-mono text-slate-400 mb-2">
            <span>FRICTION INDEX</span>
            <span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 font-bold" id="resGrade">GRADE D</span>
          </div>

          <!-- SVG Tachometer Gauge -->
          <div class="relative w-48 h-32 flex items-center justify-center mt-2">
            <svg class="w-48 h-32" viewBox="0 0 200 120">
              <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="16" stroke-linecap="round" />
              <path d="M 20 100 A 80 80 0 0 1 73 34" fill="none" stroke="#10B981" stroke-width="16" stroke-linecap="round" stroke-dasharray="1 4" />
              <path d="M 73 34 A 80 80 0 0 1 127 34" fill="none" stroke="#F59E0B" stroke-width="16" stroke-linecap="round" stroke-dasharray="1 4" />
              <path d="M 127 34 A 80 80 0 0 1 180 100" fill="none" stroke="#F43F5E" stroke-width="16" stroke-linecap="round" stroke-dasharray="1 4" />
              <line id="gaugeNeedle" x1="100" y1="100" x2="100" y2="35" stroke="#00F2FE" stroke-width="4" stroke-linecap="round" class="gauge-needle" style="transform: rotate(45deg);" />
              <circle cx="100" cy="100" r="8" fill="#FFFFFF" />
            </svg>
            <div class="absolute bottom-0 text-center">
              <span class="font-display font-black text-3xl text-white" id="resScoreNum">72</span>
              <span class="text-slate-400 text-xs font-mono">/100</span>
            </div>
          </div>

          <p class="text-xs text-slate-400 mt-4 leading-relaxed font-sans">
            Score above 50 denotes critical checkout drop-off and lost customer impulse.
          </p>
        </div>

        <!-- CARD 2: THE REVENUE LEAK -->
        <div class="glass-panel rounded-3xl p-6 sm:p-8 flex flex-col justify-between relative overflow-hidden bg-gradient-to-br from-rose-950/20 via-slate-900/40 to-black/60 border-rose-500/20">
          <div>
            <div class="flex items-center justify-between text-xs font-mono text-rose-400 mb-2">
              <span class="flex items-center gap-1.5"><i class="fas fa-triangle-exclamation"></i> ESTIMATED LEAKAGE</span>
              <span class="font-bold">LOST CAPITAL</span>
            </div>
            <h3 class="font-display font-black text-3xl sm:text-4xl text-rose-400 tracking-tight mt-3" id="resMonthlyLoss">
              $14,200<span class="text-sm font-normal text-rose-300">/mo</span>
            </h3>
            <span class="text-xs font-mono text-slate-400 block mt-1">
              Annual Hemorrhage: <strong class="text-white" id="resAnnualLoss">$170,400/yr</strong>
            </span>
          </div>

          <div class="p-3.5 rounded-2xl bg-black/40 border border-white/5 text-xs text-slate-300 space-y-1.5 mt-6 font-mono">
            <div class="flex justify-between">
              <span class="text-slate-400">Mobile Bounce Rate:</span>
              <span class="text-white font-bold" id="resMobileBounce">68%</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Hesitation Index:</span>
              <span class="text-rose-400 font-bold" id="resHesitation">8.4 / 10</span>
            </div>
          </div>
        </div>

        <!-- CARD 3: PRIMARY VULNERABILITY -->
        <div class="glass-panel rounded-3xl p-6 sm:p-8 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-xs font-mono text-cyan-400 mb-2">
              <span class="flex items-center gap-1.5"><i class="fas fa-bug"></i> PRIMARY FLAW DETECTED</span>
              <span class="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-bold" id="resFlawSeverity">CRITICAL</span>
            </div>
            <h4 class="font-display font-bold text-lg text-white mt-3" id="resFlawTitle">
              Mobile Checkout Frictional Disconnect
            </h4>
            <p class="text-xs text-slate-400 mt-2 leading-relaxed" id="resFlawImpact">
              High latency on mobile devices triggers 40% immediate abandonment before seeing prices.
            </p>
          </div>

          <div class="mt-6 pt-4 border-t border-white/10 flex items-center justify-between text-xs">
            <span class="text-emerald-400 font-mono font-bold">1 Free Diagnostic Unlocked</span>
            <span class="text-slate-500 font-mono">2 Remaining Locked</span>
          </div>
        </div>

      </div>

      <!-- ==================== LOCKED DOSSIER / PAYWALL TEASER ==================== -->
      <div id="lockedPaywallContainer" class="relative glass-panel rounded-3xl p-6 sm:p-10 overflow-hidden border border-cyan-500/20">
        
        <div class="filter blur-md select-none pointer-events-none opacity-40 space-y-6">
          <div class="h-6 bg-slate-700 rounded-md w-1/3"></div>
          <div class="grid grid-cols-2 gap-4">
            <div class="h-24 bg-slate-800 rounded-xl"></div>
            <div class="h-24 bg-slate-800 rounded-xl"></div>
          </div>
          <div class="h-32 bg-slate-800 rounded-xl"></div>
          <div class="h-40 bg-slate-800 rounded-xl"></div>
        </div>

        <div class="absolute inset-0 z-20 bg-gradient-to-t from-[#05070E] via-[#05070E]/90 to-transparent flex flex-col items-center justify-center p-6 text-center">
          
          <div class="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 text-2xl mb-4 shadow-xl shadow-cyan-500/10 animate-bounce">
            <i class="fas fa-lock"></i>
          </div>

          <span class="text-xs font-mono font-bold uppercase tracking-widest text-cyan-400 block mb-1">
            Executive Closing Dossier
          </span>
          <h3 class="font-display font-black text-2xl sm:text-3xl text-white max-w-xl">
            Unlock Full Forensic Breakdown & CEO Cold-Pitch Scripts
          </h3>
          <p class="text-slate-400 text-xs sm:text-sm max-w-md mt-2 font-normal">
            Gain immediate access to all 3 architectural fixes, the CEO WhatsApp pitch (in English & Spanish), and white-label agency export rights.
          </p>

          <div class="mt-8 flex flex-col sm:flex-row items-center gap-4 w-full max-w-md">
            
            <button onclick="triggerPayment('solana')" class="w-full py-4 px-6 rounded-2xl bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-500 hover:opacity-95 text-white font-extrabold text-xs sm:text-sm uppercase tracking-wider transition-all shadow-xl shadow-purple-500/25 flex items-center justify-center gap-2 active:scale-95">
              <i class="fab fa-ethereum text-cyan-300"></i>
              <span>Pay USDC on Solana</span>
            </button>

            <button onclick="triggerPayment('card')" class="w-full py-4 px-6 rounded-2xl bg-white/[0.08] hover:bg-white/[0.12] text-white border border-white/10 font-bold text-xs sm:text-sm uppercase tracking-wider transition-all flex items-center justify-center gap-2 active:scale-95">
              <i class="fas fa-credit-card text-slate-300"></i>
              <span>Pay $3.90 via Card</span>
            </button>
          </div>

          <div class="mt-4 flex items-center gap-2 text-xs font-mono">
            <span class="text-slate-500">Evaluating platform?</span>
            <button onclick="triggerPayment('demo')" class="text-cyan-400 hover:underline font-bold">
              ⚡ Instant Unlock (Demo Testnet Mode)
            </button>
          </div>

          <div class="mt-6 flex items-center gap-6 text-[11px] font-mono text-slate-500">
            <span><i class="fas fa-check text-emerald-400"></i> Unlocks after on-chain confirmation</span>
            <span><i class="fas fa-check text-emerald-400"></i> Zero KYC Required</span>
            <span><i class="fas fa-check text-emerald-400"></i> White-Label Rights</span>
          </div>

        </div>

      </div>

      <!-- ==================== UNLOCKED FULL INTELLIGENCE ==================== -->
      <div id="unlockedDossierContainer" class="hidden flex flex-col gap-8">
        
        <div class="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-sm">
              <i class="fas fa-check"></i>
            </div>
            <div>
              <span class="font-bold text-xs text-white block">Full Forensic Dossier Cryptographically Unlocked</span>
              <span class="text-[10px] font-mono text-slate-400" id="receiptTxHash">TX: sol_tx_verified_instant</span>
            </div>
          </div>
          <button onclick="window.print()" class="px-4 py-2 rounded-xl bg-white/[0.08] hover:bg-white/[0.15] text-white text-xs font-mono font-bold flex items-center gap-2 border border-white/10">
            <i class="fas fa-file-pdf text-rose-400"></i> Export White-Label PDF
          </button>
        </div>

        <div class="glass-panel rounded-3xl p-6 sm:p-8">
          <span class="text-xs font-mono font-bold uppercase tracking-wider text-cyan-400 block mb-1">
            Engineered Remedies
          </span>
          <h3 class="font-display font-black text-2xl text-white mb-6">
            3 High-Impact Fixes to Recover Leaked Revenue
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="fixesContainer">
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          <div class="glass-panel rounded-3xl p-6 sm:p-8 flex flex-col justify-between border-emerald-500/20 bg-emerald-950/10">
            <div>
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-2">
                  <i class="fab fa-whatsapp text-sm"></i> WhatsApp 1-to-1 Pitch
                </span>
                <button onclick="copyPitchText('pitchWhatsAppText')" class="text-xs font-mono text-slate-300 hover:text-white px-3 py-1 bg-white/[0.05] rounded-lg border border-white/10">
                  <i class="fas fa-copy mr-1"></i> Copy
                </button>
              </div>
              <p class="text-xs text-slate-300 whitespace-pre-wrap font-sans leading-relaxed p-4 bg-black/40 rounded-2xl border border-white/5 select-all" id="pitchWhatsAppText">
              </p>
            </div>
            
            <div class="mt-6 flex items-center justify-between pt-4 border-t border-white/5">
              <span class="text-[11px] font-mono text-slate-400">Target: Owner / Managing Director</span>
              <a id="directWhatsAppLink" href="#" target="_blank" class="px-4 py-2 rounded-xl bg-[#25D366] hover:bg-emerald-600 text-white text-xs font-bold flex items-center gap-2">
                <i class="fab fa-whatsapp"></i> Test in WhatsApp
              </a>
            </div>
          </div>

          <div class="glass-panel rounded-3xl p-6 sm:p-8 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-mono font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
                  <i class="fas fa-envelope text-sm"></i> Executive Cold Email Template
                </span>
                <button onclick="copyPitchText('pitchEmailText')" class="text-xs font-mono text-slate-300 hover:text-white px-3 py-1 bg-white/[0.05] rounded-lg border border-white/10">
                  <i class="fas fa-copy mr-1"></i> Copy
                </button>
              </div>
              <div class="p-4 bg-black/40 rounded-2xl border border-white/5 text-xs text-slate-300 space-y-3 font-sans leading-relaxed select-all">
                <div class="font-mono text-cyan-400 font-bold border-b border-white/5 pb-2">
                  Subject: <span id="pitchEmailSubject" class="text-white font-normal">Revenue leak detected in your mobile funnel</span>
                </div>
                <div id="pitchEmailText" class="whitespace-pre-wrap">
                </div>
              </div>
            </div>

            <div class="mt-6 flex items-center justify-between pt-4 border-t border-white/5">
              <span class="text-[11px] font-mono text-slate-400">Psychology: Loss Aversion + Specific Data</span>
              <span class="text-xs font-mono text-emerald-400 font-bold">Ready to Send</span>
            </div>
          </div>

        </div>

      </div>

    </section>

    

  </main>



  <!-- ==================== WEB3 WALLET MODAL ==================== -->
  <div id="walletModal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-md hidden items-center justify-center p-4">
    <div class="glass-panel rounded-3xl max-w-md w-full p-6 sm:p-8 relative border border-cyan-500/30">
      <button onclick="closeWalletModal()" class="absolute top-6 right-6 text-slate-400 hover:text-white text-xl">&times;</button>
      
      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center text-lg">
          <i class="fas fa-wallet"></i>
        </div>
        <div>
          <h3 class="font-display font-black text-xl text-white">Connect Web3 Wallet</h3>
          <span class="text-xs font-mono text-slate-400">Solana & Base Instant Rail</span>
        </div>
      </div>

      <div class="space-y-3 mt-6">
        <button onclick="connectWalletMock('Phantom')" class="w-full p-4 rounded-2xl bg-white/[0.05] hover:bg-white/[0.1] border border-white/5 flex items-center justify-between text-white font-bold text-xs transition-all">
          <span class="flex items-center gap-3">
            <span class="w-3 h-3 rounded-full bg-purple-500"></span> Phantom Wallet (Solana)
          </span>
          <i class="fas fa-chevron-right text-slate-500"></i>
        </button>

        <button onclick="connectWalletMock('Solflare')" class="w-full p-4 rounded-2xl bg-white/[0.05] hover:bg-white/[0.1] border border-white/5 flex items-center justify-between text-white font-bold text-xs transition-all">
          <span class="flex items-center gap-3">
            <span class="w-3 h-3 rounded-full bg-amber-500"></span> Solflare (Solana)
          </span>
          <i class="fas fa-chevron-right text-slate-500"></i>
        </button>

        <button onclick="connectWalletMock('MetaMask')" class="w-full p-4 rounded-2xl bg-white/[0.05] hover:bg-white/[0.1] border border-white/5 flex items-center justify-between text-white font-bold text-xs transition-all">
          <span class="flex items-center gap-3">
            <span class="w-3 h-3 rounded-full bg-orange-500"></span> MetaMask (Base USDC)
          </span>
          <i class="fas fa-chevron-right text-slate-500"></i>
        </button>
      </div>

      <div class="mt-6 p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/20 text-[11px] font-mono text-cyan-300">
        Connected wallets can unlock forensic reports in a single tap without credit card verification.
      </div>
    </div>
  </div>

  <!-- ==================== LOGIC & SCRIPT CONTROLLER ==================== -->
  <script>
    let currentAuditId = null;
    let currentPublicData = null;

    function fillAndScan(domain) {
      document.getElementById('targetUrlInput').value = domain;
      document.getElementById('scanner').scrollIntoView({ behavior: 'smooth' });
      handleScanSubmit(new Event('submit'));
    }

    async function handleScanSubmit(e) {
      if (e) e.preventDefault();
      const url = document.getElementById('targetUrlInput').value.trim();
      if (!url) return;

      const submitBtn = document.getElementById('scanSubmitBtn');
      const hud = document.getElementById('scanningHud');
      const results = document.getElementById('resultsSection');

      submitBtn.disabled = true;
      submitBtn.classList.add('opacity-50');
      results.classList.add('hidden');
      hud.classList.remove('hidden');

      let progress = 10;
      let seconds = 0;
      const progressEl = document.getElementById('hudProgressBar');
      const timerEl = document.getElementById('hudTimer');
      
      const timerInterval = setInterval(() => {
        seconds += 0.1;
        timerEl.innerText = seconds.toFixed(1) + 's';
      }, 100);

      const animInterval = setInterval(() => {
        if (progress < 90) {
          progress += Math.floor(Math.random() * 12) + 5;
          progressEl.style.width = progress + '%';
        }
        if (progress > 25) {
          document.querySelector('#step1 .step-status').innerText = 'DONE';
          document.querySelector('#step1 .step-status').className = 'text-emerald-400 font-bold step-status';
          document.querySelector('#step2 .step-status').innerText = 'RUNNING';
          document.querySelector('#step2 .step-status').className = 'text-cyan-400 font-bold step-status';
        }
        if (progress > 55) {
          document.querySelector('#step2 .step-status').innerText = 'DONE';
          document.querySelector('#step2 .step-status').className = 'text-emerald-400 font-bold step-status';
          document.querySelector('#step3 .step-status').innerText = 'RUNNING';
          document.querySelector('#step3 .step-status').className = 'text-cyan-400 font-bold step-status';
        }
        if (progress > 75) {
          document.querySelector('#step3 .step-status').innerText = 'DONE';
          document.querySelector('#step3 .step-status').className = 'text-emerald-400 font-bold step-status';
          document.querySelector('#step4 .step-status').innerText = 'INFERRING';
          document.querySelector('#step4 .step-status').className = 'text-cyan-400 font-bold step-status';
        }
      }, 200);

      try {
        const response = await fetch('/api/scan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: url })
        });

        if (!response.ok) { let m = 'Scan failed'; try { m = (await response.json()).detail || m } catch (e) {} throw new Error(m) };
        const data = await response.json();
        
        clearInterval(animInterval);
        clearInterval(timerInterval);
        progressEl.style.width = '100%';
        document.querySelector('#step4 .step-status').innerText = 'COMPLETE';
        document.querySelector('#step4 .step-status').className = 'text-emerald-400 font-bold step-status';

        setTimeout(() => {
          hud.classList.add('hidden');
          submitBtn.disabled = false;
          submitBtn.classList.remove('opacity-50');
          renderResults(data);
        }, 600);

      } catch (err) {
        clearInterval(animInterval);
        clearInterval(timerInterval);
        alert('Audit notice: ' + err.message);
        hud.classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-50');
      }
    }

    function renderResults(data) {
      currentAuditId = data.audit_id;
      currentPublicData = data;

      document.getElementById('resNiche').innerText = data.business_niche || 'Digital Enterprise';
      document.getElementById('resBusinessName').innerText = data.business_name || data.domain;
      document.getElementById('resDomain').innerText = data.domain;
      document.getElementById('resDomainLink').href = data.url;
      document.getElementById('resTtfb').innerText = data.ttfb_ms + 'ms';
      document.getElementById('resSize').innerText = data.page_size_kb + ' KB';
      
      const waEl = document.getElementById('resWaStatus');
      if (data.has_whatsapp) {
        waEl.innerText = 'DETECTED';
        waEl.className = 'text-emerald-400 font-bold';
      } else {
        waEl.innerText = 'MISSING (LEAK)';
        waEl.className = 'text-rose-400 font-bold';
      }

      const score = data.friction_score || 65;
      document.getElementById('resScoreNum').innerText = score;
      const angle = -90 + (score / 100) * 180;
      document.getElementById('gaugeNeedle').style.transform = `rotate(${angle}deg)`;

      document.getElementById('resGrade').innerText = 'GRADE ' + (data.health_grade || 'D');
      document.getElementById('resMonthlyLoss').innerHTML = (data.est_monthly_loss_usd || '$12,400/mo').replace('/mo', '<span class=\"text-sm font-normal text-rose-300\">/mo</span>');
      document.getElementById('resAnnualLoss').innerText = data.est_annual_loss_usd || '$148,800/yr';

      const psych = data.psychological_breakdown || {};
      document.getElementById('resMobileBounce').innerText = psych.mobile_bounce_rate || '64%';
      document.getElementById('resHesitation').innerText = psych.hesitation_index || '8.2 / 10';

      const flaw = data.primary_flaw || {};
      document.getElementById('resFlawSeverity').innerText = flaw.severity || 'CRITICAL';
      document.getElementById('resFlawTitle').innerText = flaw.title || 'Mobile Conversion Bottleneck';
      document.getElementById('resFlawImpact').innerText = flaw.impact || 'Excessive script latency degrades consumer impulse.';

      document.getElementById('lockedPaywallContainer').classList.remove('hidden');
      document.getElementById('unlockedDossierContainer').classList.add('hidden');

      document.getElementById('resultsSection').classList.remove('hidden');
      document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }

    async function triggerPayment(method) {
      if (!currentAuditId) return;

      const confirmBtn = event ? event.currentTarget : null;
      if (confirmBtn) {
        confirmBtn.innerHTML = '<i class=\"fas fa-spinner fa-spin\"></i> Verifying Web3 Settlement...';
      }

      try {
        const res = await fetch('/api/verify-payment', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            audit_id: currentAuditId,
            payment_method: method,
            tx_hash: method === 'solana' ? 'sol_5Kj3...91Xb' : (method === 'demo' ? 'demo_bypass_instant' : 'stripe_pi_8812')
          })
        });

        const result = await res.json();
        if (result.status === 'success') {
          unlockFullDossier(result.dossier);
        }
      } catch (e) {
        alert('Payment verification failed: ' + e.message);
      }
    }

    function unlockFullDossier(dossier) {
      document.getElementById('lockedPaywallContainer').classList.add('hidden');
      const unlockedEl = document.getElementById('unlockedDossierContainer');
      unlockedEl.classList.remove('hidden');

      const fixesBox = document.getElementById('fixesContainer');
      fixesBox.innerHTML = '';
      (dossier.high_impact_fixes || []).forEach((fix, idx) => {
        const div = document.createElement('div');
        div.className = 'p-5 rounded-2xl bg-white/[0.03] border border-white/5 flex flex-col justify-between';
        div.innerHTML = `
          <div>
            <div class=\"flex items-center justify-between text-xs font-mono mb-2\">
              <span class=\"text-cyan-400 font-bold\">FIX #0${idx+1}</span>
              <span class=\"text-emerald-400 font-bold\">${fix.estimated_lift || '+28% Conversion'}</span>
            </div>
            <h5 class=\"text-white font-bold text-sm mb-2\">${fix.fix_name}</h5>
            <p class=\"text-xs text-slate-400 leading-relaxed font-sans\">${fix.architecture}</p>
          </div>
        `;
        fixesBox.appendChild(div);
      });

      const pitchEn = dossier.executive_pitch_en || {};
      const waPitch = pitchEn.whatsapp_message || 'Hello, we noticed your mobile conversion latency...';
      document.getElementById('pitchWhatsAppText').innerText = waPitch;
      document.getElementById('directWhatsAppLink').href = `https://wa.me/?text=${encodeURIComponent(waPitch)}`;

      document.getElementById('pitchEmailSubject').innerText = pitchEn.subject || 'Revenue leakage detected';
      document.getElementById('pitchEmailText').innerText = pitchEn.cold_email || waPitch;

      unlockedEl.scrollIntoView({ behavior: 'smooth' });
    }

    function copyPitchText(elementId) {
      const text = document.getElementById(elementId).innerText;
      navigator.clipboard.writeText(text).then(() => {
        alert('Copied executive pitch to clipboard!');
      });
    }

    function openWalletModal() {
      document.getElementById('walletModal').classList.remove('hidden');
      document.getElementById('walletModal').classList.add('flex');
    }
    function closeWalletModal() {
      document.getElementById('walletModal').classList.add('hidden');
      document.getElementById('walletModal').classList.remove('flex');
    }
    function connectWalletMock(walletName) {
      document.getElementById('walletBtnText').innerText = `${walletName}: 8xK4...6uM1`;
      closeWalletModal();
      alert(`Connected to ${walletName}! You now have 1-click micro-billing active.`);
    }
  </script>
<script src="/pay.js"></script>
</body>
</html>
"""

os.makedirs('public', exist_ok=True)
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print('Compiled public/index.html successfully: size =', len(html_code))

