let currentLang = localStorage.getItem('lang') || 'RU';

function applyLanguage(lang) {
    document.querySelectorAll('[data-lang-ru], [data-lang-en]').forEach(el => {
        const text = lang === 'RU' ? el.dataset.langRu : el.dataset.langEn;
        if (text !== undefined) {
            el.textContent = text;
        }
    });

    document.querySelectorAll('[data-placeholder-ru], [data-placeholder-en]').forEach(el => {
        const placeholder = lang === 'RU' ? el.dataset.placeholderRu : el.dataset.placeholderEn;
        if (placeholder !== undefined) {
            el.placeholder = placeholder;
        }
    });

    const dynamicAnnouncementsHeader = document.querySelector('[data-lang-ru][data-lang-en][data-lang-ru-query][data-lang-en-query]');
    if (dynamicAnnouncementsHeader) {
        const searchParam = new URLSearchParams(window.location.search).get('search');
        let newText = '';
        if (searchParam) {
            const prefix = lang === 'RU' ? dynamicAnnouncementsHeader.dataset.langRu + ' ' + dynamicAnnouncementsHeader.dataset.langRuQuery : dynamicAnnouncementsHeader.dataset.langEn + ' ' + dynamicAnnouncementsHeader.dataset.langEnQuery;
            newText = `${prefix} "${searchParam}"`;
        } else {
            newText = lang === 'RU' ? dynamicAnnouncementsHeader.dataset.langRu : dynamicAnnouncementsHeader.dataset.langEn;
        }
        dynamicAnnouncementsHeader.textContent = newText;
    }


    const langBtn = document.getElementById('language-toggle');
    if (langBtn) {
        langBtn.textContent = lang;
    }

    localStorage.setItem('lang', lang);
    currentLang = lang;
}

function toggleLanguage(event) {
    event.preventDefault();
    const newLang = currentLang === 'RU' ? 'EN' : 'RU';
    applyLanguage(newLang);
}

document.addEventListener('DOMContentLoaded', () => {
    applyLanguage(currentLang);
});