// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.dom');
goog.require('cljs.core');
org.numenta.sanity.dom.get_bounding_page_rect = (function org$numenta$sanity$dom$get_bounding_page_rect(el){
var vec__45422 = (function (){var el__$1 = el;
var x = (0);
var y = (0);
while(true){
if(cljs.core.truth_(el__$1)){
var s = getComputedStyle(el__$1);
var include_border_QMARK_ = cljs.core.not_EQ_.cljs$core$IFn$_invoke$arity$2(s.position,"static");
var G__45429 = el__$1.offsetParent;
var G__45430 = (function (){var G__45423 = (function (){var G__45424 = (x + el__$1.offsetLeft);
if(include_border_QMARK_){
return (G__45424 + (function (){var G__45425 = s.borderLeftWidth;
return parseInt(G__45425);
})());
} else {
return G__45424;
}
})();
if(cljs.core.not_EQ_.cljs$core$IFn$_invoke$arity$2(el__$1,document.body)){
return (G__45423 - el__$1.scrollLeft);
} else {
return G__45423;
}
})();
var G__45431 = (function (){var G__45426 = (function (){var G__45427 = (y + el__$1.offsetTop);
if(include_border_QMARK_){
return (G__45427 + (function (){var G__45428 = s.borderTopWidth;
return parseInt(G__45428);
})());
} else {
return G__45427;
}
})();
if(cljs.core.not_EQ_.cljs$core$IFn$_invoke$arity$2(el__$1,document.body)){
return (G__45426 - el__$1.scrollTop);
} else {
return G__45426;
}
})();
el__$1 = G__45429;
x = G__45430;
y = G__45431;
continue;
} else {
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x,y], null);
}
break;
}
})();
var left = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45422,(0),null);
var top = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45422,(1),null);
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [left,top,(left + el.offsetWidth),(top + el.offsetHeight)], null);
});
org.numenta.sanity.dom.within_element_QMARK_ = (function org$numenta$sanity$dom$within_element_QMARK_(evt,el){
var vec__45433 = org.numenta.sanity.dom.get_bounding_page_rect(el);
var left = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45433,(0),null);
var top = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45433,(1),null);
var right = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45433,(2),null);
var bottom = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45433,(3),null);
return ((evt.pageX >= left)) && ((evt.pageX < right)) && ((evt.pageY >= top)) && ((evt.pageY < bottom));
});
org.numenta.sanity.dom.nonzero_number_QMARK_ = (function org$numenta$sanity$dom$nonzero_number_QMARK_(v){
if((typeof v === 'number') && (!((v === (0))))){
return v;
} else {
return false;
}
});
org.numenta.sanity.dom.page_x = (function org$numenta$sanity$dom$page_x(evt){
var or__6153__auto__ = evt.pageX;
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
var doc = document.documentElement;
var body = document.body;
return (evt.clientX + ((function (){var or__6153__auto____$1 = org.numenta.sanity.dom.nonzero_number_QMARK_((function (){var and__6141__auto__ = doc;
if(cljs.core.truth_(and__6141__auto__)){
return doc.scrollLeft;
} else {
return and__6141__auto__;
}
})());
if(cljs.core.truth_(or__6153__auto____$1)){
return or__6153__auto____$1;
} else {
var or__6153__auto____$2 = org.numenta.sanity.dom.nonzero_number_QMARK_((function (){var and__6141__auto__ = body;
if(cljs.core.truth_(and__6141__auto__)){
return body.scrollLeft;
} else {
return and__6141__auto__;
}
})());
if(cljs.core.truth_(or__6153__auto____$2)){
return or__6153__auto____$2;
} else {
return (0);
}
}
})() - (function (){var or__6153__auto____$1 = org.numenta.sanity.dom.nonzero_number_QMARK_((function (){var and__6141__auto__ = doc;
if(cljs.core.truth_(and__6141__auto__)){
return doc.clientLeft;
} else {
return and__6141__auto__;
}
})());
if(cljs.core.truth_(or__6153__auto____$1)){
return or__6153__auto____$1;
} else {
var or__6153__auto____$2 = org.numenta.sanity.dom.nonzero_number_QMARK_((function (){var and__6141__auto__ = body;
if(cljs.core.truth_(and__6141__auto__)){
return body.clientLeft;
} else {
return and__6141__auto__;
}
})());
if(cljs.core.truth_(or__6153__auto____$2)){
return or__6153__auto____$2;
} else {
return (0);
}
}
})()));
}
});
org.numenta.sanity.dom.page_y = (function org$numenta$sanity$dom$page_y(evt){
var or__6153__auto__ = evt.pageY;
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
var doc = document.documentElement;
var body = document.body;
return (evt.clientY + ((function (){var or__6153__auto____$1 = org.numenta.sanity.dom.nonzero_number_QMARK_((function (){var and__6141__auto__ = doc;
if(cljs.core.truth_(and__6141__auto__)){
return doc.scrollTop;
} else {
return and__6141__auto__;
}
})());
if(cljs.core.truth_(or__6153__auto____$1)){
return or__6153__auto____$1;
} else {
var or__6153__auto____$2 = org.numenta.sanity.dom.nonzero_number_QMARK_((function (){var and__6141__auto__ = body;
if(cljs.core.truth_(and__6141__auto__)){
return body.scrollTop;
} else {
return and__6141__auto__;
}
})());
if(cljs.core.truth_(or__6153__auto____$2)){
return or__6153__auto____$2;
} else {
return (0);
}
}
})() - (function (){var or__6153__auto____$1 = org.numenta.sanity.dom.nonzero_number_QMARK_((function (){var and__6141__auto__ = doc;
if(cljs.core.truth_(and__6141__auto__)){
return doc.clientTop;
} else {
return and__6141__auto__;
}
})());
if(cljs.core.truth_(or__6153__auto____$1)){
return or__6153__auto____$1;
} else {
var or__6153__auto____$2 = org.numenta.sanity.dom.nonzero_number_QMARK_((function (){var and__6141__auto__ = body;
if(cljs.core.truth_(and__6141__auto__)){
return body.clientTop;
} else {
return and__6141__auto__;
}
})());
if(cljs.core.truth_(or__6153__auto____$2)){
return or__6153__auto____$2;
} else {
return (0);
}
}
})()));
}
});
org.numenta.sanity.dom.offset_from = (function org$numenta$sanity$dom$offset_from(evt,el){
var vec__45435 = org.numenta.sanity.dom.get_bounding_page_rect(el);
var left = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45435,(0),null);
var top = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45435,(1),null);
var right = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45435,(2),null);
var bottom = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45435,(3),null);
return new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$x,(org.numenta.sanity.dom.page_x(evt) - left),cljs.core.cst$kw$y,(org.numenta.sanity.dom.page_y(evt) - top)], null);
});
org.numenta.sanity.dom.offset_from_target = (function org$numenta$sanity$dom$offset_from_target(evt){
return org.numenta.sanity.dom.offset_from(evt,evt.target);
});
