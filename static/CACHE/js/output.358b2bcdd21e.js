jQuery(function($){var path=window.location.href;$('.portal-nav-item a').each(function(){if(this.href===path.split('?')[0]){$(this).addClass('active');}});});$(document).ready(function(){$('#BrowserRequest24hDataTable').DataTable({"language":{"emptyTable":"Couldn't retrieve country traffic data due to low/no traffic"}})});$(document).ready(function(){$('#HourlyRequestDataTable').DataTable({pageLength:24,paging:false,searching:false,})});$(document).ready(function(){$('#BrowserMap24hDataTable').DataTable({"language":{"emptyTable":"Couldn't retrieve browser traffic data due to low/no traffic"}})});$(document).ready(function(){$('#FirewallEventsDataTable').DataTable({"language":{"emptyTable":"There were no threats detected by the firewall"}})});function isEven(value){if(value%2==0)
return true;else
return false;}
var sidenav_control_counter=0
function sidenav_control_toggle(){sidenav_control_counter++;if(isEven(sidenav_control_counter)){}else{$(".sidenav").addClass("d-flex")
$(".sidenav").addClass("w-100")
$(".sidenav").addClass("high-z-index")}};;$(document).ready(function(){$('.toast-notifications').toast('show');});AOS.init({disable:false,startEvent:'DOMContentLoaded',initClassName:'aos-init',animatedClassName:'aos-animate',useClassNames:false,disableMutationObserver:false,debounceDelay:50,throttleDelay:99,offset:0,delay:0,duration:400,easing:'ease',once:false,mirror:false,anchorPlacement:'center-bottom',});function isOnScreen(elem){if(elem.length==0){return;}
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
$(".main-nav-container").removeClass("animate__animated animate__slideInDown")
$(".nav-sticky-border").removeClass("nav-sticky-border-style")}
else{$(".main-nav-container").addClass("animate__animated animate__slideInDown")
$(".nav-sticky-border").addClass("nav-sticky-border-style")
$(".main-nav-container").removeClass("position-relative")
$(".main-nav-container").addClass("position-sticky")
$(".main-nav-container").addClass("top-0")
$(".main-nav-container").addClass("main-nav-sticky")}});});$("label").addClass("form-label")
$("input").addClass("form-control")
$("textarea").addClass("form-control")
$("input").addClass("form-control")
$("input.form-check-input").removeClass("form-control")
function enterClientPortal(){window.location='/portal/login'+'?returnTo='+window.location.href;return false}
function exitClientPortal(){const urlParams=new URLSearchParams(window.location.search);const returnToURL=urlParams.get('returnTo')
if(returnToURL==null){window.location="/";return false}
window.location=returnToURL;return false}
$(document).ready(function(){if(window.location.hash.length>0){window.scrollTo(0,$(window.location.hash).offset().top);}});;Sentry.init({dsn:"",integrations:[new Sentry.Integrations.BrowserTracing()],tracesSampleRate:1.0,release:"1.0.0",environment:"development",});;