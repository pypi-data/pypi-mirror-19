// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.selection');
goog.require('cljs.core');
org.numenta.sanity.selection.blank_selection = cljs.core.PersistentVector.EMPTY;
org.numenta.sanity.selection.sense = (function org$numenta$sanity$selection$sense(sel1){
var vec__46219 = cljs.core.cst$kw$path.cljs$core$IFn$_invoke$arity$1(sel1);
var t = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46219,(0),null);
var a1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46219,(1),null);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(t,cljs.core.cst$kw$senses)){
return a1;
} else {
return null;
}
});
org.numenta.sanity.selection.layer = (function org$numenta$sanity$selection$layer(sel1){
var vec__46221 = cljs.core.cst$kw$path.cljs$core$IFn$_invoke$arity$1(sel1);
var t = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46221,(0),null);
var a1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46221,(1),null);
var a2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46221,(2),null);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(t,cljs.core.cst$kw$regions)){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [a1,a2], null);
} else {
return null;
}
});
org.numenta.sanity.selection.clear = (function org$numenta$sanity$selection$clear(sel){
return cljs.core.conj.cljs$core$IFn$_invoke$arity$2(cljs.core.empty(sel),cljs.core.select_keys(cljs.core.peek(sel),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$dt,cljs.core.cst$kw$path,cljs.core.cst$kw$step], null)));
});
