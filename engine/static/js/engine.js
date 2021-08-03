$(document).ready(function(){
    $('.toast-notifications').toast('show');
});

// You can also pass an optional settings object
// below listed default settings
AOS.init({
    // Global settings:
    disable: false, // accepts following values: 'phone', 'tablet', 'mobile', boolean, expression or function
    startEvent: 'DOMContentLoaded', // name of the event dispatched on the document, that AOS should initialize on
    initClassName: 'aos-init', // class applied after initialization
    animatedClassName: 'aos-animate', // class applied on animation
    useClassNames: false, // if true, will add content of `data-aos` as classes on scroll
    disableMutationObserver: false, // disables automatic mutations' detections (advanced)
    debounceDelay: 50, // the delay on debounce used while resizing window (advanced)
    throttleDelay: 99, // the delay on throttle used while scrolling the page (advanced)
    
  
    // Settings that can be overridden on per-element basis, by `data-aos-*` attributes:
    offset: 0, // offset (in px) from the original trigger point
    delay: 0, // values from 0 to 3000, with step 50ms
    duration: 400, // values from 0 to 3000, with step 50ms
    easing: 'ease', // default easing for AOS animations
    once: false, // whether animation should happen only once - while scrolling down
    mirror: false, // whether elements should animate out while scrolling past them
    anchorPlacement: 'center-bottom', // defines which position of the element regarding to window should trigger the animation
  
});

function isOnScreen(elem) {
	// if the element doesn't exist, abort
	if( elem.length == 0 ) {
		return;
	}
	var $window = jQuery(window)
	var viewport_top = $window.scrollTop()
	var viewport_height = $window.height()
	var viewport_bottom = viewport_top + viewport_height
	var $elem = jQuery(elem)
	var top = $elem.offset().top
	var height = $elem.height()
	var bottom = top + height

	return (top >= viewport_top && top < viewport_bottom) ||
	(bottom > viewport_top && bottom <= viewport_bottom) ||
	(height > viewport_height && top <= viewport_top && bottom >= viewport_bottom)
}

jQuery( document ).ready( function() {
    window.addEventListener('scroll', function(e) {
        if( isOnScreen( jQuery( '.hero-container' ) ) ) {
            // in view
            $(".main-nav-container").addClass("position-relative")
            $(".main-nav-container").removeClass("position-sticky")
            $(".main-nav-container").removeClass("top-0")
            $(".main-nav-container").removeClass("main-nav-sticky")
            $(".main-nav-container").removeClass("animate__animated animate__slideInDown")
            $(".nav-sticky-border").removeClass("nav-sticky-border-style")
        }
        else {
            // out of view
            $(".main-nav-container").addClass("animate__animated animate__slideInDown")
            $(".nav-sticky-border").addClass("nav-sticky-border-style")
            $(".main-nav-container").removeClass("position-relative")
            $(".main-nav-container").addClass("position-sticky")
            $(".main-nav-container").addClass("top-0")
            $(".main-nav-container").addClass("main-nav-sticky")
        }
    });
});

$("label").addClass("form-label")
$("input").addClass("form-control")
$("textarea").addClass("form-control")
$("input").addClass("form-control")

$("input.form-check-input").removeClass("form-control")


function enterClientPortal() {
    window.location='/portal/login'+ '?returnTo=' + window.location.href;
    return false
}

function exitClientPortal() {
    const urlParams = new URLSearchParams(window.location.search);
    const returnToURL = urlParams.get('returnTo')
    if (returnToURL == null) {
        window.location="/";
        return false
    }
    window.location=returnToURL;
    return false
}

$(document).ready(function() {
    if(window.location.hash.length > 0) {
        window.scrollTo(0, $(window.location.hash).offset().top);
    }
});


var $ = jQuery.noConflict();
$(document).ready(function($) {

var menu_height = $('.main-nav-container').height(); // calulate the height of the menu

(function(document, history, location) {
  var HISTORY_SUPPORT = !!(history && history.pushState);

  var anchorScrolls = {
    ANCHOR_REGEX: /^#[^ ]+$/,
    OFFSET_HEIGHT_PX: menu_height, // Set the offset with the dynamic value

    /**
     * Establish events, and fix initial scroll position if a hash is provided.
     */
    init: function() {
      this.scrollIfAnchor(location.hash);
      $('body').on('click', 'a', $.proxy(this, 'delegateAnchors'));
    },

    /**
     * Return the offset amount to deduct from the normal scroll position.
     * Modify as appropriate to allow for dynamic calculations
     */
    getFixedOffset: function() {
      return this.OFFSET_HEIGHT_PX;
    },

    /**
     * If the provided href is an anchor which resolves to an element on the
     * page, scroll to it.
     * @param  {String} href
     * @return {Boolean} - Was the href an anchor.
     */
    scrollIfAnchor: function(href, pushToHistory) {
      var match, anchorOffset;

      if(!this.ANCHOR_REGEX.test(href)) {
        return false;
      }

      match = document.getElementById(href.slice(1));

      if(match) {
        anchorOffset = $(match).offset().top - this.getFixedOffset();
        $('html, body').animate({ scrollTop: anchorOffset});

        // Add the state to history as-per normal anchor links
        if(HISTORY_SUPPORT && pushToHistory) {
          history.pushState({}, document.title, location.pathname + href);
        }
      }

      return !!match;
    },

    /**
     * If the click event's target was an anchor, fix the scroll position.
     */
    delegateAnchors: function(e) {
      var elem = e.target;

      if(this.scrollIfAnchor(elem.getAttribute('href'), true)) {
        e.preventDefault();
      }
    }
  };

    $(document).ready($.proxy(anchorScrolls, 'init'));
})(window.document, window.history, window.location);
});
