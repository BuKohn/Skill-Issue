/**
 * Получает язык из cookies (приоритет) или localStorage (fallback).
 * Cookies имеют приоритет, так как они синхронизированы с сервером.
 */
function getLanguage() {
    // Сначала проверяем cookie (синхронизировано с сервером)
    const cookieLang = getCookie('lang');
    if (cookieLang && (cookieLang === 'RU' || cookieLang === 'EN')) {
        // Синхронизируем localStorage с cookie
        localStorage.setItem('lang', cookieLang);
        return cookieLang;
    }
    
    // Если cookie нет, проверяем localStorage
    const localLang = localStorage.getItem('lang');
    if (localLang && (localLang === 'RU' || localLang === 'EN')) {
        // Если есть в localStorage, но нет в cookie - отправляем на сервер
        sendLanguageToServer(localLang);
        return localLang;
    }
    
    // По умолчанию возвращаем RU
    return 'RU';
}

let currentLang = getLanguage();

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
        } else {
            // После успешного сохранения на сервере, cookie будет установлен автоматически
            // Обновляем localStorage для синхронизации
            localStorage.setItem('lang', lang);
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
    // Обновляем текстовое содержимое элементов
    document.querySelectorAll('[data-lang-ru], [data-lang-en]').forEach(el => {
        const text = lang === 'RU' ? el.dataset.langRu : el.dataset.langEn;
        if (text !== undefined) {
            // Для input элементов используем value, для остальных - textContent
            if (el.tagName === 'INPUT') {
                // Для input type="submit" или type="button" обновляем value
                if (el.type === 'submit' || el.type === 'button') {
                    el.value = text;
                } else {
                    // Для остальных input элементов обновляем textContent (если это возможно)
                    // Обычно для input используется value, но если это не submit/button, то это текстовое поле
                    // и его значение не должно меняться автоматически
                    el.textContent = text;
                }
            } else if (el.tagName === 'BUTTON') {
                el.textContent = text;
            } else {
                el.textContent = text;
            }
        }
    });

    // Обновляем placeholder для input элементов
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