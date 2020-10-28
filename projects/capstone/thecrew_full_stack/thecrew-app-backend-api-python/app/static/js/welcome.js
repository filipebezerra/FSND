jQuery(document).ready(function ($) {

  // Header fixed and Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 10) {
      $('#header').addClass('header-fixed');
    } else {
      $('#header').removeClass('header-fixed');
    }

    var target = $(this.hash);
    if (target.length) {
      var top_space = 0;

      if ($('#header').length) {
        top_space = $('#header').outerHeight();

        if (!$('#header').hasClass('header-fixed')) {
          top_space = top_space - 20;
        }
      }

      $('html, body').animate({
        scrollTop: target.offset().top - top_space
      }, 1500, 'easeInOutExpo');
      return false;
    }
  });

  // Initiate the AOS animation library
  AOS.init();

  // custom code

  // Instantiate clipboard.js
  var clipboard = new ClipboardJS('#copy-access-token');

  clipboard.on('success', function (e) {
    $('#copy-access-token').attr('data-original-title', 'Copied!');
    $('#copy-access-token').tooltip({
      placement: 'bottom',
      title: 'Copied!',
      trigger: 'hover'
    }).tooltip('enable').tooltip('show');

    e.clearSelection();
  });

  clipboard.on('error', function (e) {
    console.error('Action:', e.action);
    console.error('Trigger:', e.trigger);
  });

  $('#copy-access-token').on('hidden.bs.tooltip', function () {
    $(this).attr('data-original-title', 'Click to copy');
    $(this).tooltip('disable');
  });

  function getHashURLParam(param) {
    const hash = window.location.hash.substr(1);
    if (hash && hash !== '') {
      const prs = hash.split('&').reduce(function (res, item) {
        const parts = item.split('=');
        res[parts[0]] = parts[1];
        return res;
      }, {});
      return prs[param];
    }
  }

  const accessToken = getHashURLParam('access_token');
  if (accessToken && accessToken !== '') {
    $('#copy-access-token').attr('data-clipboard-text', accessToken);
    $('#copy-access-token').removeClass('invisible');
  }
});