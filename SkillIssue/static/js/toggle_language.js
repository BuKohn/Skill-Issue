let currentLang = localStorage.getItem('lang') || 'RU';

async function sendLanguageToServer(lang) {
    try {
        const response = await fetch('/api/set-language/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ language: lang }),
            credentials: 'same-origin'
        });

        if (!response.ok) {
            console.warn('Не удалось сохранить язык на сервере');
        }
    } catch (error) {
        console.error('Ошибка при отправке языка на сервер:', error);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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
            const prefix = lang === 'RU'
                ? dynamicAnnouncementsHeader.dataset.langRu + ' ' + dynamicAnnouncementsHeader.dataset.langRuQuery
                : dynamicAnnouncementsHeader.dataset.langEn + ' ' + dynamicAnnouncementsHeader.dataset.langEnQuery;
            newText = `${prefix} "${searchParam}"`;
        } else {
            newText = lang === 'RU'
                ? dynamicAnnouncementsHeader.dataset.langRu
                : dynamicAnnouncementsHeader.dataset.langEn;
        }
        dynamicAnnouncementsHeader.textContent = newText;
    }

    const langBtn = document.getElementById('language-toggle');
    if (langBtn) {
        langBtn.textContent = lang;
    }

    localStorage.setItem('lang', lang);
    currentLang = lang;

    sendLanguageToServer(lang);

    window.dispatchEvent(new Event('languageChanged'));
}

function toggleLanguage(event) {
    if (event) event.preventDefault();
    const newLang = currentLang === 'RU' ? 'EN' : 'RU';
    applyLanguage(newLang);
}

document.addEventListener('DOMContentLoaded', () => {
    applyLanguage(currentLang);
});