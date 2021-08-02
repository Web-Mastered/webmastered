function isOnScreen(elem){if(elem.length==0){return;}
var $window=jQuery(window)
var viewport_top=$window.scrollTop()
var viewport_height=$window.height()
var viewport_bottom=viewport_top+viewport_height
var $elem=jQuery(elem)
var top=$elem.offset().top
var height=$elem.height()
var bottom=top+height
return(top>=viewport_top&&top<viewport_bottom)||(bottom>viewport_top&&bottom<=viewport_bottom)||(height>viewport_height&&top<=viewport_top&&bottom>=viewport_bottom)}
jQuery(document).ready(function(){window.addEventListener('scroll',function(e){if(isOnScreen(jQuery('.hero-container'))){$(".main-nav-container").addClass("position-relative")
$(".main-nav-container").removeClass("position-sticky")
$(".main-nav-container").removeClass("top-0")
$(".main-nav-container").removeClass("main-nav-sticky")
$(".main-nav-container").removeClass("animate__animated animate__slideInDown")}
else{$(".main-nav-container").addClass("animate__animated animate__slideInDown")
$(".main-nav-container").removeClass("position-relative")
$(".main-nav-container").addClass("position-sticky")
$(".main-nav-container").addClass("top-0")
$(".main-nav-container").addClass("main-nav-sticky")
toast_status=toast_status+1;}});});;Sentry.init({dsn:"",integrations:[new Sentry.Integrations.BrowserTracing()],tracesSampleRate:1.0,release:"1.0.0",environment:"development",});AOS.init({disable:false,startEvent:'startAOS',initClassName:'aos-init',animatedClassName:'aos-animate',useClassNames:false,disableMutationObserver:false,debounceDelay:50,throttleDelay:99,offset:0,delay:0,duration:400,easing:'ease',once:false,mirror:false,anchorPlacement:'center-bottom',});$(document).ready(function(){setTimeout(function(){document.dispatchEvent(new Event('startAOS'));},2000);});;