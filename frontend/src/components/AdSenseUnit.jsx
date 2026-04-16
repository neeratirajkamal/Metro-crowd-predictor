import React, { useEffect } from 'react';
const AdSenseUnit = () => {
    useEffect(() => {
          const initializeAd = () => {
                  try {
                            if (window.adsbygoogle && typeof window.adsbygoogle.push === 'function') {
                                        window.adsbygoogle.push({});
                            } else {
                                        setTimeout(initializeAd, 1000);
                            }
                  } catch (e) {
                            console.warn('AdSense unit delay/error:', e);
                  }
          };
          initializeAd();
    }, []);
    return (
          <div className="mt-8 pt-6 border-t border-white/5">
                <div className="p-4 bg-slate-900/50 rounded-2xl border border-white/5 overflow-hidden">
                        <p className="text-[9px] font-black text-slate-500 uppercase mb-4 tracking-widest text-center">Advertisement</p>p>
                        <ins
                                    className="adsbygoogle"
                                    style={{ display: 'block' }}
                                    data-ad-client="ca-pub-9394912868880521"
                                    data-ad-slot="3429840664"
                                    data-ad-format="auto"
                                    data-full-width-responsive="true"
                                  ></ins>ins>
                </div>div>
          </div>div>
        );
};
export default AdSenseUnit;
</div>
