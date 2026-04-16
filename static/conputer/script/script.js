// function scrollSlider(distance) {
//     const slider = document.getElementById('slider');
//     if (slider) {
//         slider.scrollBy({
//             left: distance,
//             behavior: 'smooth'
//         });
//     }
// }
var selected = null;
document.addEventListener('click',function(e)
{
    console.log(e.target)
    console.log(e.target.classList)
    if(e.target.classList.contains('sortblock'))
    {
        elems = document.querySelectorAll('.sortblock');
        elems.forEach(element => {
            element.style.backgroundColor = ' rgba(255, 255, 255, 0)'
        });
        e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.36)';
        const pa = e.target.querySelector('.sortname');
        selected = e.target;
        console.log(pa.textContent);
        sendSort(pa.textContent);
    }

    if (e.target.classList.contains('details')) {
        const modalId = e.target.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }

    if (e.target.classList.contains('close') || e.target.classList.contains('modal-overlay')) {
        const modal = e.target.closest('.modal-overlay');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }
    
    if (e.target.classList.contains('info_btn')) {
        console.log("wow");
        const modalId = e.target.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }

    if (e.target.classList.contains('modal-overlay') || e.target.classList.contains('close')) {
        const modal = e.target.closest('.modal-overlay');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }


    if(e.target.classList.contains('formbut'))
    {
        elems = document.querySelectorAll('.formbut');
        elems.forEach(element => {
            element.style.backgroundColor = ' #26262694'
        });
        e.target.style.backgroundColor = '#26262634';
        selected = e.target;
        console.log(e.target.textContent);
        sendSort(e.target.textContent.replace(/[0-9]/g, '').trim());
    }
})

function sendSort(text) {
    const url = new URL(window.location.href);
    
    url.searchParams.set('category_name', text);
    
    window.location.href = url.toString();
}

function updateFilters(key, value) {
    const url = new URL(window.location.href);
    
    if (url.searchParams.get(key) === value) {
        url.searchParams.delete(key);
    } else {
        url.searchParams.set(key, value);
    }
    
    window.location.href = url.toString();
}


function pick(id, name) {
    // 1. Устанавливаем значение в скрытый select Django
    const select = document.getElementsByName(currentField)[0];
    select.value = id;

    // 2. Обновляем визуальный текст в левой колонке
    document.getElementById('val-' + currentField).textContent = name;
}



function liveSearch() {
    const searchInput = document.getElementById('component-search').value.toLowerCase();
    const cards = document.querySelectorAll('.sidebar-card'); // Твои карточки справа

    cards.forEach(card => {
        // Достаем название из h3 внутри карточки
        const name = card.querySelector('h3').textContent.toLowerCase();
        
        // Проверяем: совпадает ли текст И выбрана ли сейчас нужная категория (если она активна)
        const isVisibleCategory = card.style.display !== 'none' || card.hasAttribute('data-current-active');

        if (name.includes(searchInput)) {
            // Если мы уже фильтровали по категории, показываем только внутри неё
            // Если категорию не выбирали, просто показываем
            card.style.setProperty('display', 'block', 'important');
        } else {
            card.style.setProperty('display', 'none', 'important');
        }
    });
}