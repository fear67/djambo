function scrollSlider(distance) {
    const slider = document.getElementById('slider');
    slider.scrollBy({
        left: distance,
        behavior: 'smooth'
    });
}