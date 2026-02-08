// Google Analytics Integration for HydroFlow
// Tracks visitors, device types, and user behavior

export const GA_MEASUREMENT_ID = import.meta.env.VITE_GA_ID || 'G-XXXXXXXXXX';

// Initialize Google Analytics
export const initGA = () => {
    if (typeof window === 'undefined') return;

    // Load GA script
    const script = document.createElement('script');
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
    script.async = true;
    document.head.appendChild(script);

    // Initialize dataLayer
    window.dataLayer = window.dataLayer || [];
    function gtag() {
        window.dataLayer.push(arguments);
    }
    window.gtag = gtag;

    gtag('js', new Date());
    gtag('config', GA_MEASUREMENT_ID, {
        send_page_view: true,
        cookie_flags: 'SameSite=None;Secure'
    });

    console.log('📊 Analytics initialized');
};

// Track page views
export const trackPageView = (path) => {
    if (window.gtag) {
        window.gtag('config', GA_MEASUREMENT_ID, {
            page_path: path,
        });
    }
};

// Track custom events
export const trackEvent = (eventName, eventParams = {}) => {
    if (window.gtag) {
        window.gtag('event', eventName, eventParams);
    }
};

// Track view changes (Map, Dashboard, Activity)
export const trackViewChange = (viewName) => {
    trackEvent('view_change', {
        event_category: 'Navigation',
        event_label: viewName,
        value: 1
    });
};

// Track station clicks
export const trackStationClick = (stationName) => {
    trackEvent('station_click', {
        event_category: 'Interaction',
        event_label: stationName
    });
};

// Track train info views
export const trackTrainView = (trainId) => {
    trackEvent('train_view', {
        event_category: 'Interaction',
        event_label: trainId
    });
};

// Get visitor info (device type, etc.)
export const getVisitorInfo = () => {
    const userAgent = navigator.userAgent;
    const isMobile = /Mobile|Android|iPhone|iPad/i.test(userAgent);
    const isTablet = /iPad|Android/i.test(userAgent) && !/Mobile/i.test(userAgent);

    return {
        deviceType: isMobile ? 'mobile' : isTablet ? 'tablet' : 'desktop',
        platform: navigator.platform,
        language: navigator.language,
        screenSize: `${window.screen.width}x${window.screen.height}`
    };
};
