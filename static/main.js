'use strict';

/* =========================================================================
   Cookie consent banner
   ========================================================================= */

(function () {
    var COOKIE_NAME = 'cookie_consent';

    function getCookie(name) {
        var value = '; ' + document.cookie;
        var parts = value.split('; ' + name + '=');
        if (parts.length === 2) {
            return parts.pop().split(';').shift();
        }
        return null;
    }

    function setCookie(name, value, days) {
        var date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        document.cookie =
            name + '=' + value +
            '; expires=' + date.toUTCString() +
            '; path=/; SameSite=Lax';
    }

    function initBanner() {
        var banner = document.getElementById('cookie-banner');
        if (!banner) return;

        if (!getCookie(COOKIE_NAME)) {
            banner.style.display = 'block';
        }

        var acceptBtn = document.getElementById('cookie-accept');
        if (acceptBtn) {
            acceptBtn.addEventListener('click', function () {
                setCookie(COOKIE_NAME, 'accepted', 365);
                banner.style.display = 'none';
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initBanner);
    } else {
        initBanner();
    }
}());


/* =========================================================================
   Smooth scrolling for anchor links
   ========================================================================= */

(function () {
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
            anchor.addEventListener('click', function (e) {
                var targetId = this.getAttribute('href');
                if (targetId === '#') return;
                var target = document.querySelector(targetId);
                if (!target) return;
                e.preventDefault();

                /* Offset for fixed navbar */
                var navHeight = 0;
                var nav = document.querySelector('.bp-navbar');
                if (nav) navHeight = nav.offsetHeight;

                var top = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 16;
                window.scrollTo({ top: top, behavior: 'smooth' });

                /* Close mobile navbar if open */
                var collapse = document.getElementById('mainNav');
                if (collapse && collapse.classList.contains('show')) {
                    var toggler = document.querySelector('.navbar-toggler');
                    if (toggler) toggler.click();
                }
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSmoothScroll);
    } else {
        initSmoothScroll();
    }
}());


/* =========================================================================
   Active nav-link highlight on scroll (index page only)
   ========================================================================= */

(function () {
    function initScrollSpy() {
        var sections = document.querySelectorAll('section[id]');
        var navLinks = document.querySelectorAll('.navbar-nav .nav-link[href^="#"]');
        if (!sections.length || !navLinks.length) return;

        var nav = document.querySelector('.bp-navbar');
        var navHeight = nav ? nav.offsetHeight : 0;

        function onScroll() {
            var scrollPos = window.pageYOffset + navHeight + 32;
            var current = '';
            sections.forEach(function (section) {
                if (section.offsetTop <= scrollPos) {
                    current = section.getAttribute('id');
                }
            });
            navLinks.forEach(function (link) {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {
                    link.classList.add('active');
                }
            });
        }

        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScrollSpy);
    } else {
        initScrollSpy();
    }
}());
