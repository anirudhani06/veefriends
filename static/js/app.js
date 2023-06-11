const navBtns = document.querySelector('.home__grid-feed-header').children;

navBtns[0].addEventListener('click', () => {
  navBtns[0].classList.add('active');
  navBtns[1].classList.remove('active');
  navBtns[2].classList.remove('active');
  document.querySelector('.home_content').classList.add('active');
  document.querySelector('.home_messages').classList.remove('active');
  document.querySelector('.home_groups').classList.remove('active');
});
navBtns[1].addEventListener('click', () => {
  navBtns[0].classList.remove('active');
  navBtns[1].classList.add('active');
  navBtns[2].classList.remove('active');
  document.querySelector('.home_content').classList.remove('active');
  document.querySelector('.home_messages').classList.add('active');
  document.querySelector('.home_groups').classList.remove('active');
});
navBtns[2].addEventListener('click', () => {
  navBtns[0].classList.remove('active');
  navBtns[1].classList.remove('active');
  navBtns[2].classList.add('active');
  document.querySelector('.home_content').classList.remove('active');
  document.querySelector('.home_messages').classList.remove('active');
  document.querySelector('.home_groups').classList.add('active');
});
