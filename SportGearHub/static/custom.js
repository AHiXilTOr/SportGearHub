// События для меню-бургера
const burger = $(".burger");
const burgerMenu = $(".burger-menu");
const nav = $("nav");

if (burger.length && burgerMenu.length && nav.length) {
  let isOpen = false;

  burger.on("click", () => {
    burger.toggleClass("active");
    if (isOpen) {
      // Скрываем меню
      burgerMenu.css("transform", "translateY(-100%)");
      nav.css({
        opacity: 1,
        pointerEvents: "all"
      });
      isOpen = false;
    } else {
      // Показываем меню
      burgerMenu.css("transform", "translateY(0)");
      nav.css({
        opacity: 0,
        pointerEvents: "none"
      });
      isOpen = true;
    }
  });
}

// События для кнопки "раскрыть/закрыть"
const expandButton = $(".expand-button");
const expandBlock = $(".expand-block");

if (expandButton.length && expandBlock.length) {
  let isExpanded = false;

  expandButton.on("click", () => {
    if (isExpanded) {
      // Прокрутить страницу к началу блока и скрыть контент блока
      $('html, body').animate({
        scrollTop: expandBlock.offset().top - 180
      }, 500);
      expandBlock.animate({
        height: "265px"
      }, 500);
      expandButton.text("Просмотр");
      isExpanded = false;
    } else {
      // Показать контент блока при открытии
      expandBlock.animate({
        height: expandBlock.get(0).scrollHeight
      }, 500);
      expandButton.text("Закрыть");
      isExpanded = true;
    }
  });
}

// Анимация загрузки
$(window).on("load", function () {
  $("#preloader").animate(
    {
      opacity: "0", // Уменьшаем прозрачность до 0
    },
    600,
    function () {
      $("#preloader").fadeOut(); // Скрываем
    }
  );
});

function checkScreenWidth() {
  // События на фокус
  const focusHandler = function () {
    $('.logo').hide();
    $('.burger').hide();
    $('.search-field').addClass('search-field-expanded');
    $('.search-button').addClass('search-button-expanded');
  };
  // События на потерю фокуса
  const blurHandler = function () {
    $('.logo').show();
    $('.burger').show();
    $('.search-field').removeClass('search-field-expanded');
    $('.search-button').removeClass('search-button-expanded')
  };

  // Если ширина экрана меньше 663 пикселей, добавляем события
  if ($(window).width() < 663) {
    $('.search-field').on('focus', focusHandler);
    $('.search-field').on('blur', blurHandler);
  } else { // Если ширина экрана больше удаляем события
    $('.search-field').off('focus', focusHandler);
    $('.search-field').off('blur', blurHandler);
  }
}

$(document).ready(checkScreenWidth); // Вызываем функцию при загрузке страницы
$(window).on('resize', checkScreenWidth); // Добавляем функцию на изменение размера экрана

// Модальное окно
$(document).ready(function () {
  // Открываем
  $('#openModal, #openModal2, #openModal3').on('click', function () {
    $('#modal').fadeIn();
  });

  // Скрываем
  $('.close').on('click', function () {
    $('#modal').fadeOut();
  });

  // При клике за пределами модального окна скрываем его
  $(window).on('click', function (event) {
    if (event.target == $('#modal')[0]) {
      $('#modal').fadeOut();
    }
  });
});

// Отправка формы
$(document).ready(function () {
  const form = $('#feedback-form').html();
  $('#feedback-form').submit(function (event) {
    event.preventDefault(); // Прерывание процессов по умолчанию

    // Отправляем AJAX-запрос
    $.ajax({
      type: 'POST', // Метод
      url: '/create_object_view/', // Обработка сервера
      data: $(this).serialize(), // Сериализация

      success: function (response) {
        const formHtml = $('#feedback-form').html();
        if (response.success) {
          $('#feedback-form').html('<h4>Сообщение успешно отправлено!</h4>');
        } else {
          $('#feedback-form').html('<h4>Произошла ошибка при отправке сообщения. #2</h4>' + '<p>' + response.error + '</p>');
        }
      },
      error: function (response) {
        $('#feedback-form').html('<h4>Произошла ошибка при отправке сообщения. #1</h4>' + '<p>' + response.error + '</p>');
      }
    });
  }
  );
  $('#reset-btn').on('click', function () {
    $('#feedback-form').html(form) // Cброс формы
  });
});