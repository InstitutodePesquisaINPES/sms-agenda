var swiper = new Swiper(".slide-content", {
    slidesPerView: 3,
    spaceBetween: 30, 
    slidesPerGroup: 3,
    loop: true,
    loopFillGroupWithBlank: true,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});

document.addEventListener('DOMContentLoaded', function () {
    var navbar = document.getElementById('navbar');
    var lastScrollTop = 0;
  
    window.addEventListener('scroll', function() {
      var currentScrollTop = window.scrollY || document.documentElement.scrollTop;
  
      // Verifica se está no topo da página
      if (currentScrollTop === 0) {
        navbar.classList.remove('navbarToogle');
      } else if (currentScrollTop > lastScrollTop) {
        // Scroll para baixo
        navbar.classList.add('navbarToogle');
      } else if (currentScrollTop < lastScrollTop) {
        // Scroll para cima
        navbar.classList.remove('navbarToogle');
      }
  
      lastScrollTop = currentScrollTop;
    });
  });
  
  
  