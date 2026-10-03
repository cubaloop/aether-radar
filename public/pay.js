(function () {
  let TOKEN = null, PRICE = 3.9, timer = null;
  const $ = (id) => document.getElementById(id);

  const origRender = window.renderResults;
  window.renderResults = function (d) {
    TOKEN = d.token;
    origRender(d);
    let n = $('lossNote');
    if (!n) { n = document.createElement('p'); n.id = 'lossNote'; n.className = 'text-[11px] text-slate-500 mt-2 font-mono'; $('resAnnualLoss').parentElement.after(n); }
    n.textContent = 'Modeled estimate, not actual revenue. ' + (d.loss_assumptions || '');
  };

  function modal(html) {
    let m = $('payModal');
    if (!m) { m = document.createElement('div'); m.id = 'payModal'; m.className = 'fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4'; document.body.appendChild(m); }
    m.innerHTML = '<div class="glass-panel rounded-3xl max-w-md w-full p-6 text-center relative">' +
      '<button id="payClose" class="absolute top-4 right-5 text-slate-400 text-2xl">&times;</button>' + html + '</div>';
    $('payClose').onclick = () => { clearInterval(timer); m.remove(); };
  }

  window.triggerPayment = async function () {
    if (!TOKEN) return;
    modal('<p class="text-slate-300 font-mono text-sm">Preparing payment...</p>');
    let info;
    try {
      const r = await fetch('/api/pay-info', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token: TOKEN }) });
      if (!r.ok) throw new Error((await r.json()).detail || 'error');
      info = await r.json();
    } catch (e) { modal('<p class="text-rose-400">' + e.message + '</p>'); return; }
    const qr = 'https://api.qrserver.com/v1/create-qr-code/?size=220x220&margin=8&data=' + encodeURIComponent(info.uri);
    modal('<h3 class="font-display font-black text-xl text-white">Pay ' + info.amount + ' USDC on Solana</h3>' +
      '<p class="text-xs text-slate-400 mt-1">Scan with Phantom / Solflare, or open in your wallet.</p>' +
      '<img class="mx-auto my-4 rounded-xl bg-white" width="220" height="220" src="' + qr + '" alt="Solana Pay QR">' +
      '<a href="' + info.uri + '" class="block w-full py-3 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 text-white font-bold text-sm">Open in wallet</a>' +
      '<p class="text-[10px] font-mono text-slate-500 mt-3 break-all">' + info.treasury + '</p>' +
      '<p id="payStatus" class="text-xs font-mono text-cyan-300 mt-3">Waiting for on-chain confirmation...</p>');
    let tries = 0;
    clearInterval(timer);
    timer = setInterval(async () => {
      if (++tries > 150) { clearInterval(timer); const s = $('payStatus'); if (s) s.textContent = 'Timed out. Re-open payment after sending.'; return; }
      try {
        const r = await fetch('/api/verify-payment', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token: TOKEN }) });
        const d = await r.json();
        if (d.status === 'success') {
          clearInterval(timer); const m = $('payModal'); if (m) m.remove();
          window.unlockFullDossier(d.dossier);
          const rc = $('receiptTxHash'); if (rc) rc.textContent = 'TX: ' + d.tx;
        }
      } catch (e) {}
    }, 6000);
  };

  window.addEventListener('DOMContentLoaded', async () => {
    document.querySelectorAll("button[onclick*=\"'card'\"], button[onclick*=\"openWalletModal\"], #walletModal").forEach(e => e.remove());
    document.querySelectorAll("button[onclick*=\"'demo'\"]").forEach(b => b.parentElement.remove());
    try { PRICE = (await (await fetch('/api/config')).json()).pricing.audit_usdc; } catch (e) {}
    document.querySelectorAll("button[onclick*=\"'solana'\"] span").forEach(s => s.textContent = 'Pay ' + PRICE + ' USDC on Solana');
    const q = new URLSearchParams(location.search).get('scan');
    if (q) window.fillAndScan(q);
  });
})();
