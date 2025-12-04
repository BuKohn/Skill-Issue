document.addEventListener('DOMContentLoaded', function() {
    const filterToggle = document.querySelector('.filter-toggle');
    const filterDropdown = document.querySelector('.filter-dropdown');
    const filterItems = document.querySelectorAll('.filter-item');
    const currentFilterText = document.getElementById('current-filter');
    
    let activeFilter = 'all';
    
    // Показываем/скрываем меню фильтров
    filterToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        const isVisible = filterDropdown.style.display === 'block';
        filterDropdown.style.display = isVisible ? 'none' : 'block';
    });
    
    // Скрываем меню при клике вне его
    document.addEventListener('click', function() {
        filterDropdown.style.display = 'none';
    });
    
    // Обработка выбора фильтра
    filterItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.stopPropagation();
            
            // Удаляем активный класс у всех
            filterItems.forEach(i => {
                i.style.background = 'none';
                i.style.fontWeight = 'normal';
            });
            
            // Добавляем активный класс к выбранному
            this.style.background = '#f0f0f0';
            this.style.fontWeight = 'bold';
            
            // Обновляем текст на кнопке
            activeFilter = this.getAttribute('data-value');
            currentFilterText.textContent = this.textContent;
            
            // Закрываем меню
            filterDropdown.style.display = 'none';
            
            // Триггерим событие выбора фильтра
            const filterEvent = new CustomEvent('filterChanged', {
                detail: { filter: activeFilter }
            });
            document.dispatchEvent(filterEvent);
            
            console.log('Выбран фильтр:', activeFilter);
        });
    });
    
    // Предотвращаем закрытие при клике внутри меню
    filterDropdown.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});