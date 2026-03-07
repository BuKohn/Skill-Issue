document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('daysRangeSlider');
    const valueDisplay = document.getElementById('daysRangeValue');
    const filterItems = document.querySelectorAll('.filter-item');
    const currentFilter = document.getElementById('current-filter');

    // Функция склонения слов (день, дня, дней)
    function getDaysText(n) {
        if (n % 10 === 1 && n % 100 !== 11) return n + ' день';
        if (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)) return n + ' дня';
        return n + ' дней';
    }

    // Функция обновления текста ползунка
    function updateSliderValue() {
        const days = slider.value;
        valueDisplay.textContent = getDaysText(days);
    }

    // Функция установки значения ползунка из фильтра
    function setSliderFromFilter(value) {
        let days;
        switch(value) {
            case 'today': days = 1; break;
            case 'week': days = 7; break;
            case 'month': days = 30; break;
            default: days = 30;
        }
        slider.value = days;
        updateSliderValue();
    }

    // Обработчик изменения ползунка
    if (slider && valueDisplay) {
        slider.addEventListener('input', updateSliderValue);
        updateSliderValue(); // инициализация
    }

    // Обработчики для элементов фильтра (только обновление ползунка)
    filterItems.forEach(item => {
        item.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            // Обновляем ползунок при выборе пункта меню
            setSliderFromFilter(value);
        });
    });
});
