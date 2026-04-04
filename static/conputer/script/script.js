function scrollSlider(distance) {
    const slider = document.getElementById('slider');
    if (slider) {
        slider.scrollLeft += distance;
    } else {
        console.error("Элемент с id='slider' не найден!");
    }
}