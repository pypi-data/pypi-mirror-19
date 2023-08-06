// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('reagent_forms.core');
goog.require('cljs.core');
goog.require('clojure.walk');
goog.require('clojure.string');
goog.require('goog.string');
goog.require('goog.string.format');
goog.require('reagent.core');
goog.require('reagent_forms.datepicker');
reagent_forms.core.value_of = (function reagent_forms$core$value_of(element){
return element.target.value;
});
reagent_forms.core.id__GT_path = cljs.core.memoize((function (id){
var segments = clojure.string.split.cljs$core$IFn$_invoke$arity$2(cljs.core.subs.cljs$core$IFn$_invoke$arity$2([cljs.core.str(id)].join(''),(1)),/\./);
return cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.keyword,segments);
}));
reagent_forms.core.set_doc_value = (function reagent_forms$core$set_doc_value(doc,id,value,events){
var path = (reagent_forms.core.id__GT_path.cljs$core$IFn$_invoke$arity$1 ? reagent_forms.core.id__GT_path.cljs$core$IFn$_invoke$arity$1(id) : reagent_forms.core.id__GT_path.call(null,id));
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (path){
return (function (p1__66344_SHARP_,p2__66343_SHARP_){
var or__6153__auto__ = (p2__66343_SHARP_.cljs$core$IFn$_invoke$arity$3 ? p2__66343_SHARP_.cljs$core$IFn$_invoke$arity$3(path,value,p1__66344_SHARP_) : p2__66343_SHARP_.call(null,path,value,p1__66344_SHARP_));
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return p1__66344_SHARP_;
}
});})(path))
,cljs.core.assoc_in(doc,path,value),events);
});
reagent_forms.core.mk_save_fn = (function reagent_forms$core$mk_save_fn(doc,events){
return (function (id,value){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$variadic(doc,reagent_forms.core.set_doc_value,id,value,cljs.core.array_seq([events], 0));
});
});
reagent_forms.core.wrap_get_fn = (function reagent_forms$core$wrap_get_fn(get,wrapper){
return (function (id){
var G__66346 = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
return (wrapper.cljs$core$IFn$_invoke$arity$1 ? wrapper.cljs$core$IFn$_invoke$arity$1(G__66346) : wrapper.call(null,G__66346));
});
});
reagent_forms.core.wrap_save_fn = (function reagent_forms$core$wrap_save_fn(save_BANG_,wrapper){
return (function (id,value){
var G__66349 = id;
var G__66350 = (wrapper.cljs$core$IFn$_invoke$arity$1 ? wrapper.cljs$core$IFn$_invoke$arity$1(value) : wrapper.call(null,value));
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66349,G__66350) : save_BANG_.call(null,G__66349,G__66350));
});
});
reagent_forms.core.wrap_fns = (function reagent_forms$core$wrap_fns(opts,node){
return new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$doc,cljs.core.cst$kw$doc.cljs$core$IFn$_invoke$arity$1(opts),cljs.core.cst$kw$get,(function (){var temp__4655__auto__ = cljs.core.cst$kw$in_DASH_fn.cljs$core$IFn$_invoke$arity$1(cljs.core.second(node));
if(cljs.core.truth_(temp__4655__auto__)){
var in_fn = temp__4655__auto__;
return reagent_forms.core.wrap_get_fn(cljs.core.cst$kw$get.cljs$core$IFn$_invoke$arity$1(opts),in_fn);
} else {
return cljs.core.cst$kw$get.cljs$core$IFn$_invoke$arity$1(opts);
}
})(),cljs.core.cst$kw$save_BANG_,(function (){var temp__4655__auto__ = cljs.core.cst$kw$out_DASH_fn.cljs$core$IFn$_invoke$arity$1(cljs.core.second(node));
if(cljs.core.truth_(temp__4655__auto__)){
var out_fn = temp__4655__auto__;
return reagent_forms.core.wrap_save_fn(cljs.core.cst$kw$save_BANG_.cljs$core$IFn$_invoke$arity$1(opts),out_fn);
} else {
return cljs.core.cst$kw$save_BANG_.cljs$core$IFn$_invoke$arity$1(opts);
}
})()], null);
});
if(typeof reagent_forms.core.format_type !== 'undefined'){
} else {
reagent_forms.core.format_type = (function (){var method_table__7066__auto__ = (function (){var G__66351 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66351) : cljs.core.atom.call(null,G__66351));
})();
var prefer_table__7067__auto__ = (function (){var G__66352 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66352) : cljs.core.atom.call(null,G__66352));
})();
var method_cache__7068__auto__ = (function (){var G__66353 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66353) : cljs.core.atom.call(null,G__66353));
})();
var cached_hierarchy__7069__auto__ = (function (){var G__66354 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66354) : cljs.core.atom.call(null,G__66354));
})();
var hierarchy__7070__auto__ = cljs.core.get.cljs$core$IFn$_invoke$arity$3(cljs.core.PersistentArrayMap.EMPTY,cljs.core.cst$kw$hierarchy,cljs.core.get_global_hierarchy());
return (new cljs.core.MultiFn(cljs.core.symbol.cljs$core$IFn$_invoke$arity$2("reagent-forms.core","format-type"),((function (method_table__7066__auto__,prefer_table__7067__auto__,method_cache__7068__auto__,cached_hierarchy__7069__auto__,hierarchy__7070__auto__){
return (function (field_type,_){
if(cljs.core.truth_(cljs.core.some(cljs.core.PersistentHashSet.fromArray([field_type], true),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$range,cljs.core.cst$kw$numeric], null)))){
return cljs.core.cst$kw$numeric;
} else {
return field_type;
}
});})(method_table__7066__auto__,prefer_table__7067__auto__,method_cache__7068__auto__,cached_hierarchy__7069__auto__,hierarchy__7070__auto__))
,cljs.core.cst$kw$default,hierarchy__7070__auto__,method_table__7066__auto__,prefer_table__7067__auto__,method_cache__7068__auto__,cached_hierarchy__7069__auto__));
})();
}
reagent_forms.core.valid_number_ending_QMARK_ = (function reagent_forms$core$valid_number_ending_QMARK_(n){
return ((cljs.core.not_EQ_.cljs$core$IFn$_invoke$arity$2(".",cljs.core.last(cljs.core.butlast(n)))) && (cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(".",cljs.core.last(n)))) || (cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2("0",cljs.core.last(n)));
});
reagent_forms.core.format_value = (function reagent_forms$core$format_value(fmt,value){
if(cljs.core.truth_((function (){var and__6141__auto__ = cljs.core.not((function (){var G__66358 = parseFloat(value);
return isNaN(G__66358);
})());
if(and__6141__auto__){
return fmt;
} else {
return and__6141__auto__;
}
})())){
return goog.string.format(fmt,value);
} else {
return value;
}
});
reagent_forms.core.format_type.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$numeric,(function (_,n){
if(cljs.core.truth_(cljs.core.not_empty(n))){
var parsed = parseFloat(n);
if(cljs.core.truth_(isNaN(parsed))){
return null;
} else {
if(cljs.core.truth_(reagent_forms.core.valid_number_ending_QMARK_(n))){
return n;
} else {
return parsed;
}
}
} else {
return null;
}
}));
reagent_forms.core.format_type.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$default,(function (_,value){
return value;
}));
if(typeof reagent_forms.core.bind !== 'undefined'){
} else {
reagent_forms.core.bind = (function (){var method_table__7066__auto__ = (function (){var G__66359 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66359) : cljs.core.atom.call(null,G__66359));
})();
var prefer_table__7067__auto__ = (function (){var G__66360 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66360) : cljs.core.atom.call(null,G__66360));
})();
var method_cache__7068__auto__ = (function (){var G__66361 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66361) : cljs.core.atom.call(null,G__66361));
})();
var cached_hierarchy__7069__auto__ = (function (){var G__66362 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66362) : cljs.core.atom.call(null,G__66362));
})();
var hierarchy__7070__auto__ = cljs.core.get.cljs$core$IFn$_invoke$arity$3(cljs.core.PersistentArrayMap.EMPTY,cljs.core.cst$kw$hierarchy,cljs.core.get_global_hierarchy());
return (new cljs.core.MultiFn(cljs.core.symbol.cljs$core$IFn$_invoke$arity$2("reagent-forms.core","bind"),((function (method_table__7066__auto__,prefer_table__7067__auto__,method_cache__7068__auto__,cached_hierarchy__7069__auto__,hierarchy__7070__auto__){
return (function (p__66363,_){
var map__66364 = p__66363;
var map__66364__$1 = ((((!((map__66364 == null)))?((((map__66364.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66364.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66364):map__66364);
var field = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66364__$1,cljs.core.cst$kw$field);
if(cljs.core.truth_(cljs.core.some(cljs.core.PersistentHashSet.fromArray([field], true),new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$text,cljs.core.cst$kw$numeric,cljs.core.cst$kw$password,cljs.core.cst$kw$email,cljs.core.cst$kw$tel,cljs.core.cst$kw$range,cljs.core.cst$kw$textarea], null)))){
return cljs.core.cst$kw$input_DASH_field;
} else {
return field;
}
});})(method_table__7066__auto__,prefer_table__7067__auto__,method_cache__7068__auto__,cached_hierarchy__7069__auto__,hierarchy__7070__auto__))
,cljs.core.cst$kw$default,hierarchy__7070__auto__,method_table__7066__auto__,prefer_table__7067__auto__,method_cache__7068__auto__,cached_hierarchy__7069__auto__));
})();
}
reagent_forms.core.bind.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$input_DASH_field,(function (p__66367,p__66368){
var map__66369 = p__66367;
var map__66369__$1 = ((((!((map__66369 == null)))?((((map__66369.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66369.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66369):map__66369);
var field = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66369__$1,cljs.core.cst$kw$field);
var id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66369__$1,cljs.core.cst$kw$id);
var fmt = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66369__$1,cljs.core.cst$kw$fmt);
var map__66370 = p__66368;
var map__66370__$1 = ((((!((map__66370 == null)))?((((map__66370.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66370.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66370):map__66370);
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66370__$1,cljs.core.cst$kw$get);
var save_BANG_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66370__$1,cljs.core.cst$kw$save_BANG_);
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66370__$1,cljs.core.cst$kw$doc);
return new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$value,(function (){var value = (function (){var or__6153__auto__ = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return "";
}
})();
return reagent_forms.core.format_value(fmt,value);
})(),cljs.core.cst$kw$on_DASH_change,((function (map__66369,map__66369__$1,field,id,fmt,map__66370,map__66370__$1,get,save_BANG_,doc){
return (function (p1__66366_SHARP_){
var G__66375 = id;
var G__66376 = (function (){var G__66377 = field;
var G__66378 = reagent_forms.core.value_of(p1__66366_SHARP_);
return (reagent_forms.core.format_type.cljs$core$IFn$_invoke$arity$2 ? reagent_forms.core.format_type.cljs$core$IFn$_invoke$arity$2(G__66377,G__66378) : reagent_forms.core.format_type.call(null,G__66377,G__66378));
})();
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66375,G__66376) : save_BANG_.call(null,G__66375,G__66376));
});})(map__66369,map__66369__$1,field,id,fmt,map__66370,map__66370__$1,get,save_BANG_,doc))
], null);
}));
reagent_forms.core.bind.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$checkbox,(function (p__66379,p__66380){
var map__66381 = p__66379;
var map__66381__$1 = ((((!((map__66381 == null)))?((((map__66381.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66381.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66381):map__66381);
var id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66381__$1,cljs.core.cst$kw$id);
var map__66382 = p__66380;
var map__66382__$1 = ((((!((map__66382 == null)))?((((map__66382.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66382.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66382):map__66382);
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66382__$1,cljs.core.cst$kw$get);
var save_BANG_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66382__$1,cljs.core.cst$kw$save_BANG_);
return new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$checked,(get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id)),cljs.core.cst$kw$on_DASH_change,((function (map__66381,map__66381__$1,id,map__66382,map__66382__$1,get,save_BANG_){
return (function (){
var G__66385 = id;
var G__66386 = cljs.core.not((get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id)));
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66385,G__66386) : save_BANG_.call(null,G__66385,G__66386));
});})(map__66381,map__66381__$1,id,map__66382,map__66382__$1,get,save_BANG_))
], null);
}));
reagent_forms.core.bind.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$default,(function (_,___$1){
return null;
}));
reagent_forms.core.set_attrs = (function reagent_forms$core$set_attrs(var_args){
var args__7218__auto__ = [];
var len__7211__auto___66394 = arguments.length;
var i__7212__auto___66395 = (0);
while(true){
if((i__7212__auto___66395 < len__7211__auto___66394)){
args__7218__auto__.push((arguments[i__7212__auto___66395]));

var G__66396 = (i__7212__auto___66395 + (1));
i__7212__auto___66395 = G__66396;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((2) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((2)),(0))):null);
return reagent_forms.core.set_attrs.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),(arguments[(1)]),argseq__7219__auto__);
});

reagent_forms.core.set_attrs.cljs$core$IFn$_invoke$arity$variadic = (function (p__66390,opts,p__66391){
var vec__66392 = p__66390;
var type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66392,(0),null);
var attrs = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66392,(1),null);
var body = cljs.core.nthnext(vec__66392,(2));
var vec__66393 = p__66391;
var default_attrs = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66393,(0),null);
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([default_attrs,(reagent_forms.core.bind.cljs$core$IFn$_invoke$arity$2 ? reagent_forms.core.bind.cljs$core$IFn$_invoke$arity$2(attrs,opts) : reagent_forms.core.bind.call(null,attrs,opts)),attrs], 0))], null),body);
});

reagent_forms.core.set_attrs.cljs$lang$maxFixedArity = (2);

reagent_forms.core.set_attrs.cljs$lang$applyTo = (function (seq66387){
var G__66388 = cljs.core.first(seq66387);
var seq66387__$1 = cljs.core.next(seq66387);
var G__66389 = cljs.core.first(seq66387__$1);
var seq66387__$2 = cljs.core.next(seq66387__$1);
return reagent_forms.core.set_attrs.cljs$core$IFn$_invoke$arity$variadic(G__66388,G__66389,seq66387__$2);
});
if(typeof reagent_forms.core.init_field !== 'undefined'){
} else {
reagent_forms.core.init_field = (function (){var method_table__7066__auto__ = (function (){var G__66397 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66397) : cljs.core.atom.call(null,G__66397));
})();
var prefer_table__7067__auto__ = (function (){var G__66398 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66398) : cljs.core.atom.call(null,G__66398));
})();
var method_cache__7068__auto__ = (function (){var G__66399 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66399) : cljs.core.atom.call(null,G__66399));
})();
var cached_hierarchy__7069__auto__ = (function (){var G__66400 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__66400) : cljs.core.atom.call(null,G__66400));
})();
var hierarchy__7070__auto__ = cljs.core.get.cljs$core$IFn$_invoke$arity$3(cljs.core.PersistentArrayMap.EMPTY,cljs.core.cst$kw$hierarchy,cljs.core.get_global_hierarchy());
return (new cljs.core.MultiFn(cljs.core.symbol.cljs$core$IFn$_invoke$arity$2("reagent-forms.core","init-field"),((function (method_table__7066__auto__,prefer_table__7067__auto__,method_cache__7068__auto__,cached_hierarchy__7069__auto__,hierarchy__7070__auto__){
return (function (p__66401,_){
var vec__66402 = p__66401;
var ___$1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66402,(0),null);
var map__66403 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66402,(1),null);
var map__66403__$1 = ((((!((map__66403 == null)))?((((map__66403.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66403.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66403):map__66403);
var field = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66403__$1,cljs.core.cst$kw$field);
var field__$1 = cljs.core.keyword.cljs$core$IFn$_invoke$arity$1(field);
if(cljs.core.truth_(cljs.core.some(cljs.core.PersistentHashSet.fromArray([field__$1], true),new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$range,cljs.core.cst$kw$text,cljs.core.cst$kw$password,cljs.core.cst$kw$email,cljs.core.cst$kw$tel,cljs.core.cst$kw$textarea], null)))){
return cljs.core.cst$kw$input_DASH_field;
} else {
return field__$1;
}
});})(method_table__7066__auto__,prefer_table__7067__auto__,method_cache__7068__auto__,cached_hierarchy__7069__auto__,hierarchy__7070__auto__))
,cljs.core.cst$kw$default,hierarchy__7070__auto__,method_table__7066__auto__,prefer_table__7067__auto__,method_cache__7068__auto__,cached_hierarchy__7069__auto__));
})();
}
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$container,(function (p__66406,p__66407){
var vec__66408 = p__66406;
var type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66408,(0),null);
var map__66409 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66408,(1),null);
var map__66409__$1 = ((((!((map__66409 == null)))?((((map__66409.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66409.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66409):map__66409);
var attrs = map__66409__$1;
var valid_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66409__$1,cljs.core.cst$kw$valid_QMARK_);
var body = cljs.core.nthnext(vec__66408,(2));
var map__66410 = p__66407;
var map__66410__$1 = ((((!((map__66410 == null)))?((((map__66410.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66410.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66410):map__66410);
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66410__$1,cljs.core.cst$kw$doc);
return ((function (vec__66408,type,map__66409,map__66409__$1,attrs,valid_QMARK_,body,map__66410,map__66410__$1,doc){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66413 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66413) : visible__66335__auto__.call(null,G__66413));
})())){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,(function (){var temp__4655__auto____$1 = (cljs.core.truth_(valid_QMARK_)?(function (){var G__66414 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (valid_QMARK_.cljs$core$IFn$_invoke$arity$1 ? valid_QMARK_.cljs$core$IFn$_invoke$arity$1(G__66414) : valid_QMARK_.call(null,G__66414));
})():null);
if(cljs.core.truth_(temp__4655__auto____$1)){
var valid_class = temp__4655__auto____$1;
return cljs.core.update_in.cljs$core$IFn$_invoke$arity$3(attrs,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$class], null),((function (valid_class,temp__4655__auto____$1,visible__66335__auto__,temp__4655__auto__,vec__66408,type,map__66409,map__66409__$1,attrs,valid_QMARK_,body,map__66410,map__66410__$1,doc){
return (function (p1__66405_SHARP_){
if(!(cljs.core.empty_QMARK_(p1__66405_SHARP_))){
return [cljs.core.str(p1__66405_SHARP_),cljs.core.str(" "),cljs.core.str(valid_class)].join('');
} else {
return valid_class;
}
});})(valid_class,temp__4655__auto____$1,visible__66335__auto__,temp__4655__auto__,vec__66408,type,map__66409,map__66409__$1,attrs,valid_QMARK_,body,map__66410,map__66410__$1,doc))
);
} else {
return attrs;
}
})()], null),body);
} else {
return null;
}
} else {
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,(function (){var temp__4655__auto____$1 = (cljs.core.truth_(valid_QMARK_)?(function (){var G__66415 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (valid_QMARK_.cljs$core$IFn$_invoke$arity$1 ? valid_QMARK_.cljs$core$IFn$_invoke$arity$1(G__66415) : valid_QMARK_.call(null,G__66415));
})():null);
if(cljs.core.truth_(temp__4655__auto____$1)){
var valid_class = temp__4655__auto____$1;
return cljs.core.update_in.cljs$core$IFn$_invoke$arity$3(attrs,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$class], null),((function (valid_class,temp__4655__auto____$1,temp__4655__auto__,vec__66408,type,map__66409,map__66409__$1,attrs,valid_QMARK_,body,map__66410,map__66410__$1,doc){
return (function (p1__66405_SHARP_){
if(!(cljs.core.empty_QMARK_(p1__66405_SHARP_))){
return [cljs.core.str(p1__66405_SHARP_),cljs.core.str(" "),cljs.core.str(valid_class)].join('');
} else {
return valid_class;
}
});})(valid_class,temp__4655__auto____$1,temp__4655__auto__,vec__66408,type,map__66409,map__66409__$1,attrs,valid_QMARK_,body,map__66410,map__66410__$1,doc))
);
} else {
return attrs;
}
})()], null),body);
}
});
;})(vec__66408,type,map__66409,map__66409__$1,attrs,valid_QMARK_,body,map__66410,map__66410__$1,doc))
}));
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$input_DASH_field,(function (p__66416,p__66417){
var vec__66418 = p__66416;
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66418,(0),null);
var map__66419 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66418,(1),null);
var map__66419__$1 = ((((!((map__66419 == null)))?((((map__66419.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66419.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66419):map__66419);
var attrs = map__66419__$1;
var field = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66419__$1,cljs.core.cst$kw$field);
var component = vec__66418;
var map__66420 = p__66417;
var map__66420__$1 = ((((!((map__66420 == null)))?((((map__66420.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66420.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66420):map__66420);
var opts = map__66420__$1;
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66420__$1,cljs.core.cst$kw$doc);
return ((function (vec__66418,_,map__66419,map__66419__$1,attrs,field,component,map__66420,map__66420__$1,opts,doc){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66423 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66423) : visible__66335__auto__.call(null,G__66423));
})())){
return reagent_forms.core.set_attrs.cljs$core$IFn$_invoke$arity$variadic(component,opts,cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$type,field], null)], 0));
} else {
return null;
}
} else {
return reagent_forms.core.set_attrs.cljs$core$IFn$_invoke$arity$variadic(component,opts,cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$type,field], null)], 0));
}
});
;})(vec__66418,_,map__66419,map__66419__$1,attrs,field,component,map__66420,map__66420__$1,opts,doc))
}));
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$numeric,(function (p__66425,p__66426){
var vec__66427 = p__66425;
var type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66427,(0),null);
var map__66428 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66427,(1),null);
var map__66428__$1 = ((((!((map__66428 == null)))?((((map__66428.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66428.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66428):map__66428);
var attrs = map__66428__$1;
var id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66428__$1,cljs.core.cst$kw$id);
var fmt = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66428__$1,cljs.core.cst$kw$fmt);
var map__66429 = p__66426;
var map__66429__$1 = ((((!((map__66429 == null)))?((((map__66429.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66429.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66429):map__66429);
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66429__$1,cljs.core.cst$kw$doc);
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66429__$1,cljs.core.cst$kw$get);
var save_BANG_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66429__$1,cljs.core.cst$kw$save_BANG_);
var display_value = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$changed_DASH_self_QMARK_,false,cljs.core.cst$kw$value,(get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id))], null));
return ((function (display_value,vec__66427,type,map__66428,map__66428__$1,attrs,id,fmt,map__66429,map__66429__$1,doc,get,save_BANG_){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66432 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66432) : visible__66335__auto__.call(null,G__66432));
})())){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$type,cljs.core.cst$kw$text,cljs.core.cst$kw$value,(function (){var doc_value = (function (){var or__6153__auto__ = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return "";
}
})();
var map__66433 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(display_value) : cljs.core.deref.call(null,display_value));
var map__66433__$1 = ((((!((map__66433 == null)))?((((map__66433.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66433.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66433):map__66433);
var changed_self_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66433__$1,cljs.core.cst$kw$changed_DASH_self_QMARK_);
var value = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66433__$1,cljs.core.cst$kw$value);
var value__$1 = (cljs.core.truth_(changed_self_QMARK_)?value:doc_value);
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(display_value,cljs.core.dissoc,cljs.core.cst$kw$changed_DASH_self_QMARK_);

return reagent_forms.core.format_value(fmt,value__$1);
})(),cljs.core.cst$kw$on_DASH_change,((function (visible__66335__auto__,temp__4655__auto__,display_value,vec__66427,type,map__66428,map__66428__$1,attrs,id,fmt,map__66429,map__66429__$1,doc,get,save_BANG_){
return (function (p1__66424_SHARP_){
var temp__4655__auto____$1 = (function (){var G__66435 = cljs.core.cst$kw$numeric;
var G__66436 = reagent_forms.core.value_of(p1__66424_SHARP_);
return (reagent_forms.core.format_type.cljs$core$IFn$_invoke$arity$2 ? reagent_forms.core.format_type.cljs$core$IFn$_invoke$arity$2(G__66435,G__66436) : reagent_forms.core.format_type.call(null,G__66435,G__66436));
})();
if(cljs.core.truth_(temp__4655__auto____$1)){
var value = temp__4655__auto____$1;
var G__66437_66449 = display_value;
var G__66438_66450 = new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$changed_DASH_self_QMARK_,true,cljs.core.cst$kw$value,value], null);
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__66437_66449,G__66438_66450) : cljs.core.reset_BANG_.call(null,G__66437_66449,G__66438_66450));

var G__66439 = id;
var G__66440 = parseFloat(value);
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66439,G__66440) : save_BANG_.call(null,G__66439,G__66440));
} else {
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(id,null) : save_BANG_.call(null,id,null));
}
});})(visible__66335__auto__,temp__4655__auto__,display_value,vec__66427,type,map__66428,map__66428__$1,attrs,id,fmt,map__66429,map__66429__$1,doc,get,save_BANG_))
], null),attrs], 0))], null);
} else {
return null;
}
} else {
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$type,cljs.core.cst$kw$text,cljs.core.cst$kw$value,(function (){var doc_value = (function (){var or__6153__auto__ = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return "";
}
})();
var map__66441 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(display_value) : cljs.core.deref.call(null,display_value));
var map__66441__$1 = ((((!((map__66441 == null)))?((((map__66441.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66441.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66441):map__66441);
var changed_self_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66441__$1,cljs.core.cst$kw$changed_DASH_self_QMARK_);
var value = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66441__$1,cljs.core.cst$kw$value);
var value__$1 = (cljs.core.truth_(changed_self_QMARK_)?value:doc_value);
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(display_value,cljs.core.dissoc,cljs.core.cst$kw$changed_DASH_self_QMARK_);

return reagent_forms.core.format_value(fmt,value__$1);
})(),cljs.core.cst$kw$on_DASH_change,((function (temp__4655__auto__,display_value,vec__66427,type,map__66428,map__66428__$1,attrs,id,fmt,map__66429,map__66429__$1,doc,get,save_BANG_){
return (function (p1__66424_SHARP_){
var temp__4655__auto____$1 = (function (){var G__66443 = cljs.core.cst$kw$numeric;
var G__66444 = reagent_forms.core.value_of(p1__66424_SHARP_);
return (reagent_forms.core.format_type.cljs$core$IFn$_invoke$arity$2 ? reagent_forms.core.format_type.cljs$core$IFn$_invoke$arity$2(G__66443,G__66444) : reagent_forms.core.format_type.call(null,G__66443,G__66444));
})();
if(cljs.core.truth_(temp__4655__auto____$1)){
var value = temp__4655__auto____$1;
var G__66445_66451 = display_value;
var G__66446_66452 = new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$changed_DASH_self_QMARK_,true,cljs.core.cst$kw$value,value], null);
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__66445_66451,G__66446_66452) : cljs.core.reset_BANG_.call(null,G__66445_66451,G__66446_66452));

var G__66447 = id;
var G__66448 = parseFloat(value);
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66447,G__66448) : save_BANG_.call(null,G__66447,G__66448));
} else {
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(id,null) : save_BANG_.call(null,id,null));
}
});})(temp__4655__auto__,display_value,vec__66427,type,map__66428,map__66428__$1,attrs,id,fmt,map__66429,map__66429__$1,doc,get,save_BANG_))
], null),attrs], 0))], null);
}
});
;})(display_value,vec__66427,type,map__66428,map__66428__$1,attrs,id,fmt,map__66429,map__66429__$1,doc,get,save_BANG_))
}));
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$datepicker,(function (p__66454,p__66455){
var vec__66456 = p__66454;
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66456,(0),null);
var map__66457 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66456,(1),null);
var map__66457__$1 = ((((!((map__66457 == null)))?((((map__66457.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66457.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66457):map__66457);
var attrs = map__66457__$1;
var id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66457__$1,cljs.core.cst$kw$id);
var date_format = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66457__$1,cljs.core.cst$kw$date_DASH_format);
var inline = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66457__$1,cljs.core.cst$kw$inline);
var auto_close_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66457__$1,cljs.core.cst$kw$auto_DASH_close_QMARK_);
var map__66458 = p__66455;
var map__66458__$1 = ((((!((map__66458 == null)))?((((map__66458.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66458.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66458):map__66458);
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66458__$1,cljs.core.cst$kw$doc);
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66458__$1,cljs.core.cst$kw$get);
var save_BANG_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66458__$1,cljs.core.cst$kw$save_BANG_);
var fmt = reagent_forms.datepicker.parse_format(date_format);
var today = (new Date());
var expanded_QMARK_ = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(false);
return ((function (fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66461 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66461) : visible__66335__auto__.call(null,G__66461));
})())){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$datepicker_DASH_wrapper,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$input_DASH_group$date,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([attrs,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$read_DASH_only,true,cljs.core.cst$kw$type,cljs.core.cst$kw$text,cljs.core.cst$kw$on_DASH_click,((function (visible__66335__auto__,temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_){
return (function (){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(expanded_QMARK_,cljs.core.not);
});})(visible__66335__auto__,temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$value,(function (){var temp__4657__auto__ = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
if(cljs.core.truth_(temp__4657__auto__)){
var date = temp__4657__auto__;
return reagent_forms.datepicker.format_date(date,fmt);
} else {
return null;
}
})()], null)], 0))], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$span$input_DASH_group_DASH_addon,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,((function (visible__66335__auto__,temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_){
return (function (){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(expanded_QMARK_,cljs.core.not);
});})(visible__66335__auto__,temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_))
], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$i$glyphicon$glyphicon_DASH_calendar], null)], null)], null),new cljs.core.PersistentVector(null, 9, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.datepicker.datepicker,today.getFullYear(),today.getMonth(),today.getDate(),expanded_QMARK_,auto_close_QMARK_,((function (visible__66335__auto__,temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_){
return (function (){
return (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
});})(visible__66335__auto__,temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_))
,((function (visible__66335__auto__,temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_){
return (function (p1__66453_SHARP_){
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(id,p1__66453_SHARP_) : save_BANG_.call(null,id,p1__66453_SHARP_));
});})(visible__66335__auto__,temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_))
,inline], null)], null);
} else {
return null;
}
} else {
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$datepicker_DASH_wrapper,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$input_DASH_group$date,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([attrs,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$read_DASH_only,true,cljs.core.cst$kw$type,cljs.core.cst$kw$text,cljs.core.cst$kw$on_DASH_click,((function (temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_){
return (function (){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(expanded_QMARK_,cljs.core.not);
});})(temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$value,(function (){var temp__4657__auto__ = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
if(cljs.core.truth_(temp__4657__auto__)){
var date = temp__4657__auto__;
return reagent_forms.datepicker.format_date(date,fmt);
} else {
return null;
}
})()], null)], 0))], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$span$input_DASH_group_DASH_addon,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,((function (temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_){
return (function (){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(expanded_QMARK_,cljs.core.not);
});})(temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_))
], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$i$glyphicon$glyphicon_DASH_calendar], null)], null)], null),new cljs.core.PersistentVector(null, 9, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.datepicker.datepicker,today.getFullYear(),today.getMonth(),today.getDate(),expanded_QMARK_,auto_close_QMARK_,((function (temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_){
return (function (){
return (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
});})(temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_))
,((function (temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_){
return (function (p1__66453_SHARP_){
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(id,p1__66453_SHARP_) : save_BANG_.call(null,id,p1__66453_SHARP_));
});})(temp__4655__auto__,fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_))
,inline], null)], null);
}
});
;})(fmt,today,expanded_QMARK_,vec__66456,_,map__66457,map__66457__$1,attrs,id,date_format,inline,auto_close_QMARK_,map__66458,map__66458__$1,doc,get,save_BANG_))
}));
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$checkbox,(function (p__66462,p__66463){
var vec__66464 = p__66462;
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66464,(0),null);
var map__66465 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66464,(1),null);
var map__66465__$1 = ((((!((map__66465 == null)))?((((map__66465.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66465.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66465):map__66465);
var attrs = map__66465__$1;
var id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66465__$1,cljs.core.cst$kw$id);
var field = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66465__$1,cljs.core.cst$kw$field);
var component = vec__66464;
var map__66466 = p__66463;
var map__66466__$1 = ((((!((map__66466 == null)))?((((map__66466.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66466.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66466):map__66466);
var opts = map__66466__$1;
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66466__$1,cljs.core.cst$kw$doc);
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66466__$1,cljs.core.cst$kw$get);
return ((function (vec__66464,_,map__66465,map__66465__$1,attrs,id,field,component,map__66466,map__66466__$1,opts,doc,get){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66469 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66469) : visible__66335__auto__.call(null,G__66469));
})())){
return reagent_forms.core.set_attrs.cljs$core$IFn$_invoke$arity$variadic(component,opts,cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$type,field], null)], 0));
} else {
return null;
}
} else {
return reagent_forms.core.set_attrs.cljs$core$IFn$_invoke$arity$variadic(component,opts,cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$type,field], null)], 0));
}
});
;})(vec__66464,_,map__66465,map__66465__$1,attrs,id,field,component,map__66466,map__66466__$1,opts,doc,get))
}));
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$label,(function (p__66470,p__66471){
var vec__66472 = p__66470;
var type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66472,(0),null);
var map__66473 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66472,(1),null);
var map__66473__$1 = ((((!((map__66473 == null)))?((((map__66473.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66473.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66473):map__66473);
var attrs = map__66473__$1;
var id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66473__$1,cljs.core.cst$kw$id);
var preamble = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66473__$1,cljs.core.cst$kw$preamble);
var postamble = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66473__$1,cljs.core.cst$kw$postamble);
var placeholder = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66473__$1,cljs.core.cst$kw$placeholder);
var map__66474 = p__66471;
var map__66474__$1 = ((((!((map__66474 == null)))?((((map__66474.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66474.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66474):map__66474);
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66474__$1,cljs.core.cst$kw$doc);
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66474__$1,cljs.core.cst$kw$get);
return ((function (vec__66472,type,map__66473,map__66473__$1,attrs,id,preamble,postamble,placeholder,map__66474,map__66474__$1,doc,get){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66477 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66477) : visible__66335__auto__.call(null,G__66477));
})())){
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,attrs,preamble,(function (){var temp__4655__auto____$1 = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
if(cljs.core.truth_(temp__4655__auto____$1)){
var value = temp__4655__auto____$1;
return [cljs.core.str(value),cljs.core.str(postamble)].join('');
} else {
return placeholder;
}
})()], null);
} else {
return null;
}
} else {
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,attrs,preamble,(function (){var temp__4655__auto____$1 = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
if(cljs.core.truth_(temp__4655__auto____$1)){
var value = temp__4655__auto____$1;
return [cljs.core.str(value),cljs.core.str(postamble)].join('');
} else {
return placeholder;
}
})()], null);
}
});
;})(vec__66472,type,map__66473,map__66473__$1,attrs,id,preamble,postamble,placeholder,map__66474,map__66474__$1,doc,get))
}));
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$alert,(function (p__66478,p__66479){
var vec__66480 = p__66478;
var type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66480,(0),null);
var map__66481 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66480,(1),null);
var map__66481__$1 = ((((!((map__66481 == null)))?((((map__66481.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66481.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66481):map__66481);
var attrs = map__66481__$1;
var id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66481__$1,cljs.core.cst$kw$id);
var event = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66481__$1,cljs.core.cst$kw$event);
var touch_event = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66481__$1,cljs.core.cst$kw$touch_DASH_event);
var body = cljs.core.nthnext(vec__66480,(2));
var map__66482 = p__66479;
var map__66482__$1 = ((((!((map__66482 == null)))?((((map__66482.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66482.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66482):map__66482);
var opts = map__66482__$1;
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66482__$1,cljs.core.cst$kw$doc);
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66482__$1,cljs.core.cst$kw$get);
var save_BANG_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66482__$1,cljs.core.cst$kw$save_BANG_);
return ((function (vec__66480,type,map__66481,map__66481__$1,attrs,id,event,touch_event,body,map__66482,map__66482__$1,opts,doc,get,save_BANG_){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66485 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66485) : visible__66335__auto__.call(null,G__66485));
})())){
if(cljs.core.truth_(event)){
if(cljs.core.truth_((function (){var G__66486 = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
return (event.cljs$core$IFn$_invoke$arity$1 ? event.cljs$core$IFn$_invoke$arity$1(G__66486) : event.call(null,G__66486));
})())){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(attrs,event)], null),body);
} else {
return null;
}
} else {
var temp__4655__auto____$1 = cljs.core.not_empty((get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id)));
if(cljs.core.truth_(temp__4655__auto____$1)){
var message = temp__4655__auto____$1;
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,attrs,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$close,cljs.core.PersistentArrayMap.fromArray([cljs.core.cst$kw$type,"button",cljs.core.cst$kw$aria_DASH_hidden,true,(function (){var or__6153__auto__ = touch_event;
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return cljs.core.cst$kw$on_DASH_click;
}
})(),((function (message,temp__4655__auto____$1,visible__66335__auto__,temp__4655__auto__,vec__66480,type,map__66481,map__66481__$1,attrs,id,event,touch_event,body,map__66482,map__66482__$1,opts,doc,get,save_BANG_){
return (function (){
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(id,null) : save_BANG_.call(null,id,null));
});})(message,temp__4655__auto____$1,visible__66335__auto__,temp__4655__auto__,vec__66480,type,map__66481,map__66481__$1,attrs,id,event,touch_event,body,map__66482,map__66482__$1,opts,doc,get,save_BANG_))
], true, false),"X"], null),message], null);
} else {
return null;
}
}
} else {
return null;
}
} else {
if(cljs.core.truth_(event)){
if(cljs.core.truth_((function (){var G__66487 = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
return (event.cljs$core$IFn$_invoke$arity$1 ? event.cljs$core$IFn$_invoke$arity$1(G__66487) : event.call(null,G__66487));
})())){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(attrs,event)], null),body);
} else {
return null;
}
} else {
var temp__4655__auto____$1 = cljs.core.not_empty((get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id)));
if(cljs.core.truth_(temp__4655__auto____$1)){
var message = temp__4655__auto____$1;
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,attrs,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$close,cljs.core.PersistentArrayMap.fromArray([cljs.core.cst$kw$type,"button",cljs.core.cst$kw$aria_DASH_hidden,true,(function (){var or__6153__auto__ = touch_event;
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return cljs.core.cst$kw$on_DASH_click;
}
})(),((function (message,temp__4655__auto____$1,temp__4655__auto__,vec__66480,type,map__66481,map__66481__$1,attrs,id,event,touch_event,body,map__66482,map__66482__$1,opts,doc,get,save_BANG_){
return (function (){
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(id,null) : save_BANG_.call(null,id,null));
});})(message,temp__4655__auto____$1,temp__4655__auto__,vec__66480,type,map__66481,map__66481__$1,attrs,id,event,touch_event,body,map__66482,map__66482__$1,opts,doc,get,save_BANG_))
], true, false),"X"], null),message], null);
} else {
return null;
}
}
}
});
;})(vec__66480,type,map__66481,map__66481__$1,attrs,id,event,touch_event,body,map__66482,map__66482__$1,opts,doc,get,save_BANG_))
}));
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$radio,(function (p__66488,p__66489){
var vec__66490 = p__66488;
var type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66490,(0),null);
var map__66491 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66490,(1),null);
var map__66491__$1 = ((((!((map__66491 == null)))?((((map__66491.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66491.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66491):map__66491);
var attrs = map__66491__$1;
var field = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66491__$1,cljs.core.cst$kw$field);
var name = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66491__$1,cljs.core.cst$kw$name);
var value = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66491__$1,cljs.core.cst$kw$value);
var body = cljs.core.nthnext(vec__66490,(2));
var map__66492 = p__66489;
var map__66492__$1 = ((((!((map__66492 == null)))?((((map__66492.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66492.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66492):map__66492);
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66492__$1,cljs.core.cst$kw$doc);
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66492__$1,cljs.core.cst$kw$get);
var save_BANG_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66492__$1,cljs.core.cst$kw$save_BANG_);
return ((function (vec__66490,type,map__66491,map__66491__$1,attrs,field,name,value,body,map__66492,map__66492__$1,doc,get,save_BANG_){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66495 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66495) : visible__66335__auto__.call(null,G__66495));
})())){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$type,cljs.core.cst$kw$radio,cljs.core.cst$kw$checked,cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(value,(get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(name) : get.call(null,name))),cljs.core.cst$kw$on_DASH_change,((function (visible__66335__auto__,temp__4655__auto__,vec__66490,type,map__66491,map__66491__$1,attrs,field,name,value,body,map__66492,map__66492__$1,doc,get,save_BANG_){
return (function (){
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(name,value) : save_BANG_.call(null,name,value));
});})(visible__66335__auto__,temp__4655__auto__,vec__66490,type,map__66491,map__66491__$1,attrs,field,name,value,body,map__66492,map__66492__$1,doc,get,save_BANG_))
], null),attrs], 0))], null),body);
} else {
return null;
}
} else {
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$type,cljs.core.cst$kw$radio,cljs.core.cst$kw$checked,cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(value,(get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(name) : get.call(null,name))),cljs.core.cst$kw$on_DASH_change,((function (temp__4655__auto__,vec__66490,type,map__66491,map__66491__$1,attrs,field,name,value,body,map__66492,map__66492__$1,doc,get,save_BANG_){
return (function (){
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(name,value) : save_BANG_.call(null,name,value));
});})(temp__4655__auto__,vec__66490,type,map__66491,map__66491__$1,attrs,field,name,value,body,map__66492,map__66492__$1,doc,get,save_BANG_))
], null),attrs], 0))], null),body);
}
});
;})(vec__66490,type,map__66491,map__66491__$1,attrs,field,name,value,body,map__66492,map__66492__$1,doc,get,save_BANG_))
}));
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$typeahead,(function (p__66499,p__66500){
var vec__66501 = p__66499;
var type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66501,(0),null);
var map__66502 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66501,(1),null);
var map__66502__$1 = ((((!((map__66502 == null)))?((((map__66502.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66502.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66502):map__66502);
var attrs = map__66502__$1;
var id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66502__$1,cljs.core.cst$kw$id);
var data_source = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66502__$1,cljs.core.cst$kw$data_DASH_source);
var input_class = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66502__$1,cljs.core.cst$kw$input_DASH_class);
var list_class = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66502__$1,cljs.core.cst$kw$list_DASH_class);
var item_class = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66502__$1,cljs.core.cst$kw$item_DASH_class);
var highlight_class = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66502__$1,cljs.core.cst$kw$highlight_DASH_class);
var result_fn = cljs.core.get.cljs$core$IFn$_invoke$arity$3(map__66502__$1,cljs.core.cst$kw$result_DASH_fn,cljs.core.identity);
var choice_fn = cljs.core.get.cljs$core$IFn$_invoke$arity$3(map__66502__$1,cljs.core.cst$kw$choice_DASH_fn,cljs.core.identity);
var clear_on_focus_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$3(map__66502__$1,cljs.core.cst$kw$clear_DASH_on_DASH_focus_QMARK_,true);
var map__66503 = p__66500;
var map__66503__$1 = ((((!((map__66503 == null)))?((((map__66503.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66503.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66503):map__66503);
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66503__$1,cljs.core.cst$kw$doc);
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66503__$1,cljs.core.cst$kw$get);
var save_BANG_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66503__$1,cljs.core.cst$kw$save_BANG_);
var typeahead_hidden_QMARK_ = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(true);
var mouse_on_list_QMARK_ = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(false);
var selected_index = reagent.core.atom.cljs$core$IFn$_invoke$arity$1((0));
var selections = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.PersistentVector.EMPTY);
var choose_selected = ((function (typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
var choice_66529 = cljs.core.nth.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selections) : cljs.core.deref.call(null,selections)),(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selected_index) : cljs.core.deref.call(null,selected_index)));
(save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(id,choice_66529) : save_BANG_.call(null,id,choice_66529));

(choice_fn.cljs$core$IFn$_invoke$arity$1 ? choice_fn.cljs$core$IFn$_invoke$arity$1(choice_66529) : choice_fn.call(null,choice_66529));

return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(typeahead_hidden_QMARK_,true) : cljs.core.reset_BANG_.call(null,typeahead_hidden_QMARK_,true));
});})(typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
;
return ((function (typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66506 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66506) : visible__66335__auto__.call(null,G__66506));
})())){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input,new cljs.core.PersistentArrayMap(null, 7, [cljs.core.cst$kw$type,cljs.core.cst$kw$text,cljs.core.cst$kw$class,input_class,cljs.core.cst$kw$value,(function (){var v = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
if(!(cljs.core.iterable_QMARK_(v))){
return v;
} else {
return cljs.core.first(v);
}
})(),cljs.core.cst$kw$on_DASH_focus,((function (visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
if(cljs.core.truth_(clear_on_focus_QMARK_)){
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(id,"") : save_BANG_.call(null,id,""));
} else {
return null;
}
});})(visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$on_DASH_blur,((function (visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
if(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(mouse_on_list_QMARK_) : cljs.core.deref.call(null,mouse_on_list_QMARK_)))){
return null;
} else {
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(typeahead_hidden_QMARK_,true) : cljs.core.reset_BANG_.call(null,typeahead_hidden_QMARK_,true));

return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(selected_index,(0)) : cljs.core.reset_BANG_.call(null,selected_index,(0)));
}
});})(visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$on_DASH_change,((function (visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (p1__66496_SHARP_){
var G__66508_66530 = selections;
var G__66509_66531 = (function (){var G__66510 = reagent_forms.core.value_of(p1__66496_SHARP_).toLowerCase();
return (data_source.cljs$core$IFn$_invoke$arity$1 ? data_source.cljs$core$IFn$_invoke$arity$1(G__66510) : data_source.call(null,G__66510));
})();
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__66508_66530,G__66509_66531) : cljs.core.reset_BANG_.call(null,G__66508_66530,G__66509_66531));

var G__66511_66532 = id;
var G__66512_66533 = reagent_forms.core.value_of(p1__66496_SHARP_);
(save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66511_66532,G__66512_66533) : save_BANG_.call(null,G__66511_66532,G__66512_66533));

(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(typeahead_hidden_QMARK_,false) : cljs.core.reset_BANG_.call(null,typeahead_hidden_QMARK_,false));

return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(selected_index,(0)) : cljs.core.reset_BANG_.call(null,selected_index,(0)));
});})(visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$on_DASH_key_DASH_down,((function (visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (p1__66497_SHARP_){
var G__66513 = p1__66497_SHARP_.which;
switch (G__66513) {
case (38):
p1__66497_SHARP_.preventDefault();

if(!(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selected_index) : cljs.core.deref.call(null,selected_index)),(0)))){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(selected_index,cljs.core.dec);
} else {
return null;
}

break;
case (40):
p1__66497_SHARP_.preventDefault();

if(!(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selected_index) : cljs.core.deref.call(null,selected_index)),(cljs.core.count((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selections) : cljs.core.deref.call(null,selections))) - (1))))){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(selected_index,cljs.core.inc);
} else {
return null;
}

break;
case (9):
return choose_selected();

break;
case (13):
return choose_selected();

break;
case (27):
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(typeahead_hidden_QMARK_,true) : cljs.core.reset_BANG_.call(null,typeahead_hidden_QMARK_,true));

return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(selected_index,(0)) : cljs.core.reset_BANG_.call(null,selected_index,(0)));

break;
default:
return "default";

}
});})(visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$ul,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$display,(cljs.core.truth_((function (){var or__6153__auto__ = cljs.core.empty_QMARK_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selections) : cljs.core.deref.call(null,selections)));
if(or__6153__auto__){
return or__6153__auto__;
} else {
return (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(typeahead_hidden_QMARK_) : cljs.core.deref.call(null,typeahead_hidden_QMARK_));
}
})())?cljs.core.cst$kw$none:cljs.core.cst$kw$block)], null),cljs.core.cst$kw$class,list_class,cljs.core.cst$kw$on_DASH_mouse_DASH_enter,((function (visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(mouse_on_list_QMARK_,true) : cljs.core.reset_BANG_.call(null,mouse_on_list_QMARK_,true));
});})(visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$on_DASH_mouse_DASH_leave,((function (visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(mouse_on_list_QMARK_,false) : cljs.core.reset_BANG_.call(null,mouse_on_list_QMARK_,false));
});})(visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
], null),cljs.core.doall.cljs$core$IFn$_invoke$arity$1(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(((function (visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (index,result){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$li,new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$tab_DASH_index,index,cljs.core.cst$kw$key,index,cljs.core.cst$kw$class,((cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selected_index) : cljs.core.deref.call(null,selected_index)),index))?highlight_class:item_class),cljs.core.cst$kw$on_DASH_mouse_DASH_over,((function (visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (p1__66498_SHARP_){
var G__66515 = selected_index;
var G__66516 = (function (){var G__66517 = p1__66498_SHARP_.target.getAttribute("tabIndex");
return parseInt(G__66517);
})();
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__66515,G__66516) : cljs.core.reset_BANG_.call(null,G__66515,G__66516));
});})(visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$on_DASH_click,((function (visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(typeahead_hidden_QMARK_,true) : cljs.core.reset_BANG_.call(null,typeahead_hidden_QMARK_,true));

(save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(id,result) : save_BANG_.call(null,id,result));

return (choice_fn.cljs$core$IFn$_invoke$arity$1 ? choice_fn.cljs$core$IFn$_invoke$arity$1(result) : choice_fn.call(null,result));
});})(visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
], null),(result_fn.cljs$core$IFn$_invoke$arity$1 ? result_fn.cljs$core$IFn$_invoke$arity$1(result) : result_fn.call(null,result))], null);
});})(visible__66335__auto__,temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selections) : cljs.core.deref.call(null,selections))))], null)], null);
} else {
return null;
}
} else {
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input,new cljs.core.PersistentArrayMap(null, 7, [cljs.core.cst$kw$type,cljs.core.cst$kw$text,cljs.core.cst$kw$class,input_class,cljs.core.cst$kw$value,(function (){var v = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
if(!(cljs.core.iterable_QMARK_(v))){
return v;
} else {
return cljs.core.first(v);
}
})(),cljs.core.cst$kw$on_DASH_focus,((function (temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
if(cljs.core.truth_(clear_on_focus_QMARK_)){
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(id,"") : save_BANG_.call(null,id,""));
} else {
return null;
}
});})(temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$on_DASH_blur,((function (temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
if(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(mouse_on_list_QMARK_) : cljs.core.deref.call(null,mouse_on_list_QMARK_)))){
return null;
} else {
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(typeahead_hidden_QMARK_,true) : cljs.core.reset_BANG_.call(null,typeahead_hidden_QMARK_,true));

return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(selected_index,(0)) : cljs.core.reset_BANG_.call(null,selected_index,(0)));
}
});})(temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$on_DASH_change,((function (temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (p1__66496_SHARP_){
var G__66519_66535 = selections;
var G__66520_66536 = (function (){var G__66521 = reagent_forms.core.value_of(p1__66496_SHARP_).toLowerCase();
return (data_source.cljs$core$IFn$_invoke$arity$1 ? data_source.cljs$core$IFn$_invoke$arity$1(G__66521) : data_source.call(null,G__66521));
})();
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__66519_66535,G__66520_66536) : cljs.core.reset_BANG_.call(null,G__66519_66535,G__66520_66536));

var G__66522_66537 = id;
var G__66523_66538 = reagent_forms.core.value_of(p1__66496_SHARP_);
(save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66522_66537,G__66523_66538) : save_BANG_.call(null,G__66522_66537,G__66523_66538));

(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(typeahead_hidden_QMARK_,false) : cljs.core.reset_BANG_.call(null,typeahead_hidden_QMARK_,false));

return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(selected_index,(0)) : cljs.core.reset_BANG_.call(null,selected_index,(0)));
});})(temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$on_DASH_key_DASH_down,((function (temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (p1__66497_SHARP_){
var G__66524 = p1__66497_SHARP_.which;
switch (G__66524) {
case (38):
p1__66497_SHARP_.preventDefault();

if(!(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selected_index) : cljs.core.deref.call(null,selected_index)),(0)))){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(selected_index,cljs.core.dec);
} else {
return null;
}

break;
case (40):
p1__66497_SHARP_.preventDefault();

if(!(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selected_index) : cljs.core.deref.call(null,selected_index)),(cljs.core.count((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selections) : cljs.core.deref.call(null,selections))) - (1))))){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(selected_index,cljs.core.inc);
} else {
return null;
}

break;
case (9):
return choose_selected();

break;
case (13):
return choose_selected();

break;
case (27):
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(typeahead_hidden_QMARK_,true) : cljs.core.reset_BANG_.call(null,typeahead_hidden_QMARK_,true));

return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(selected_index,(0)) : cljs.core.reset_BANG_.call(null,selected_index,(0)));

break;
default:
return "default";

}
});})(temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$ul,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$display,(cljs.core.truth_((function (){var or__6153__auto__ = cljs.core.empty_QMARK_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selections) : cljs.core.deref.call(null,selections)));
if(or__6153__auto__){
return or__6153__auto__;
} else {
return (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(typeahead_hidden_QMARK_) : cljs.core.deref.call(null,typeahead_hidden_QMARK_));
}
})())?cljs.core.cst$kw$none:cljs.core.cst$kw$block)], null),cljs.core.cst$kw$class,list_class,cljs.core.cst$kw$on_DASH_mouse_DASH_enter,((function (temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(mouse_on_list_QMARK_,true) : cljs.core.reset_BANG_.call(null,mouse_on_list_QMARK_,true));
});})(temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$on_DASH_mouse_DASH_leave,((function (temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(mouse_on_list_QMARK_,false) : cljs.core.reset_BANG_.call(null,mouse_on_list_QMARK_,false));
});})(temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
], null),cljs.core.doall.cljs$core$IFn$_invoke$arity$1(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(((function (temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (index,result){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$li,new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$tab_DASH_index,index,cljs.core.cst$kw$key,index,cljs.core.cst$kw$class,((cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selected_index) : cljs.core.deref.call(null,selected_index)),index))?highlight_class:item_class),cljs.core.cst$kw$on_DASH_mouse_DASH_over,((function (temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (p1__66498_SHARP_){
var G__66526 = selected_index;
var G__66527 = (function (){var G__66528 = p1__66498_SHARP_.target.getAttribute("tabIndex");
return parseInt(G__66528);
})();
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__66526,G__66527) : cljs.core.reset_BANG_.call(null,G__66526,G__66527));
});})(temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,cljs.core.cst$kw$on_DASH_click,((function (temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_){
return (function (){
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(typeahead_hidden_QMARK_,true) : cljs.core.reset_BANG_.call(null,typeahead_hidden_QMARK_,true));

(save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(id,result) : save_BANG_.call(null,id,result));

return (choice_fn.cljs$core$IFn$_invoke$arity$1 ? choice_fn.cljs$core$IFn$_invoke$arity$1(result) : choice_fn.call(null,result));
});})(temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
], null),(result_fn.cljs$core$IFn$_invoke$arity$1 ? result_fn.cljs$core$IFn$_invoke$arity$1(result) : result_fn.call(null,result))], null);
});})(temp__4655__auto__,typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
,(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selections) : cljs.core.deref.call(null,selections))))], null)], null);
}
});
;})(typeahead_hidden_QMARK_,mouse_on_list_QMARK_,selected_index,selections,choose_selected,vec__66501,type,map__66502,map__66502__$1,attrs,id,data_source,input_class,list_class,item_class,highlight_class,result_fn,choice_fn,clear_on_focus_QMARK_,map__66503,map__66503__$1,doc,get,save_BANG_))
}));
reagent_forms.core.group_item = (function reagent_forms$core$group_item(p__66540,p__66541,selections,field,id){
var vec__66571 = p__66540;
var type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66571,(0),null);
var map__66572 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66571,(1),null);
var map__66572__$1 = ((((!((map__66572 == null)))?((((map__66572.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66572.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66572):map__66572);
var attrs = map__66572__$1;
var key = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66572__$1,cljs.core.cst$kw$key);
var touch_event = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66572__$1,cljs.core.cst$kw$touch_DASH_event);
var body = cljs.core.nthnext(vec__66571,(2));
var map__66573 = p__66541;
var map__66573__$1 = ((((!((map__66573 == null)))?((((map__66573.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66573.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66573):map__66573);
var save_BANG_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66573__$1,cljs.core.cst$kw$save_BANG_);
var multi_select = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66573__$1,cljs.core.cst$kw$multi_DASH_select);
var handle_click_BANG_ = ((function (vec__66571,type,map__66572,map__66572__$1,attrs,key,touch_event,body,map__66573,map__66573__$1,save_BANG_,multi_select){
return (function reagent_forms$core$group_item_$_handle_click_BANG_(){
if(cljs.core.truth_(multi_select)){
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(selections,cljs.core.update_in,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [key], null),cljs.core.not);

var G__66594 = id;
var G__66595 = cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.first,cljs.core.filter.cljs$core$IFn$_invoke$arity$2(cljs.core.second,(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selections) : cljs.core.deref.call(null,selections))));
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66594,G__66595) : save_BANG_.call(null,G__66594,G__66595));
} else {
var value = cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selections) : cljs.core.deref.call(null,selections)),key);
var G__66596_66600 = selections;
var G__66597_66601 = cljs.core.PersistentArrayMap.fromArray([key,cljs.core.not(value)], true, false);
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__66596_66600,G__66597_66601) : cljs.core.reset_BANG_.call(null,G__66596_66600,G__66597_66601));

var G__66598 = id;
var G__66599 = (cljs.core.truth_(cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selections) : cljs.core.deref.call(null,selections)),key))?key:null);
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66598,G__66599) : save_BANG_.call(null,G__66598,G__66599));
}
});})(vec__66571,type,map__66572,map__66572__$1,attrs,key,touch_event,body,map__66573,map__66573__$1,save_BANG_,multi_select))
;
return ((function (vec__66571,type,map__66572,map__66572__$1,attrs,key,touch_event,body,map__66573,map__66573__$1,save_BANG_,multi_select){
return (function (){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.PersistentArrayMap.fromArray([cljs.core.cst$kw$class,(cljs.core.truth_(cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selections) : cljs.core.deref.call(null,selections)),key))?"active":null),(function (){var or__6153__auto__ = touch_event;
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return cljs.core.cst$kw$on_DASH_click;
}
})(),handle_click_BANG_], true, false),attrs], 0)),body], null);
});
;})(vec__66571,type,map__66572,map__66572__$1,attrs,key,touch_event,body,map__66573,map__66573__$1,save_BANG_,multi_select))
});
reagent_forms.core.mk_selections = (function reagent_forms$core$mk_selections(id,selectors,p__66602){
var map__66609 = p__66602;
var map__66609__$1 = ((((!((map__66609 == null)))?((((map__66609.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66609.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66609):map__66609);
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66609__$1,cljs.core.cst$kw$get);
var multi_select = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66609__$1,cljs.core.cst$kw$multi_DASH_select);
var value = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (value,map__66609,map__66609__$1,get,multi_select){
return (function (m,p__66611){
var vec__66612 = p__66611;
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66612,(0),null);
var map__66613 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66612,(1),null);
var map__66613__$1 = ((((!((map__66613 == null)))?((((map__66613.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66613.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66613):map__66613);
var key = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66613__$1,cljs.core.cst$kw$key);
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(m,key,cljs.core.boolean$(cljs.core.some(cljs.core.PersistentHashSet.fromArray([key], true),(cljs.core.truth_(multi_select)?value:new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [value], null)))));
});})(value,map__66609,map__66609__$1,get,multi_select))
,cljs.core.PersistentArrayMap.EMPTY,selectors);
});
/**
 * selectors might be passed in inline or as a collection
 */
reagent_forms.core.extract_selectors = (function reagent_forms$core$extract_selectors(selectors){
if((cljs.core.ffirst(selectors) instanceof cljs.core.Keyword)){
return selectors;
} else {
return cljs.core.first(selectors);
}
});
reagent_forms.core.selection_group = (function reagent_forms$core$selection_group(p__66617,p__66618){
var vec__66629 = p__66617;
var type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66629,(0),null);
var map__66630 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66629,(1),null);
var map__66630__$1 = ((((!((map__66630 == null)))?((((map__66630.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66630.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66630):map__66630);
var attrs = map__66630__$1;
var field = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66630__$1,cljs.core.cst$kw$field);
var id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66630__$1,cljs.core.cst$kw$id);
var selection_items = cljs.core.nthnext(vec__66629,(2));
var map__66631 = p__66618;
var map__66631__$1 = ((((!((map__66631 == null)))?((((map__66631.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66631.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66631):map__66631);
var opts = map__66631__$1;
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66631__$1,cljs.core.cst$kw$get);
var selection_items__$1 = reagent_forms.core.extract_selectors(selection_items);
var selections = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(reagent_forms.core.mk_selections(id,selection_items__$1,opts));
var selectors = cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (selection_items__$1,selections,vec__66629,type,map__66630,map__66630__$1,attrs,field,id,selection_items,map__66631,map__66631__$1,opts,get){
return (function (item){
return new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$visible_QMARK_,cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(cljs.core.second(item)),cljs.core.cst$kw$selector,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.core.group_item(item,opts,selections,field,id)], null)], null);
});})(selection_items__$1,selections,vec__66629,type,map__66630,map__66630__$1,attrs,field,id,selection_items,map__66631,map__66631__$1,opts,get))
,selection_items__$1);
return ((function (selection_items__$1,selections,selectors,vec__66629,type,map__66630,map__66630__$1,attrs,field,id,selection_items,map__66631,map__66631__$1,opts,get){
return (function (){
if(cljs.core.truth_((get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id)))){
} else {
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(selections,((function (selection_items__$1,selections,selectors,vec__66629,type,map__66630,map__66630__$1,attrs,field,id,selection_items,map__66631,map__66631__$1,opts,get){
return (function (p1__66615_SHARP_){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (selection_items__$1,selections,selectors,vec__66629,type,map__66630,map__66630__$1,attrs,field,id,selection_items,map__66631,map__66631__$1,opts,get){
return (function (p__66634){
var vec__66635 = p__66634;
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66635,(0),null);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [k,false], null);
});})(selection_items__$1,selections,selectors,vec__66629,type,map__66630,map__66630__$1,attrs,field,id,selection_items,map__66631,map__66631__$1,opts,get))
,p1__66615_SHARP_));
});})(selection_items__$1,selections,selectors,vec__66629,type,map__66630,map__66630__$1,attrs,field,id,selection_items,map__66631,map__66631__$1,opts,get))
);
}

return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,attrs], null),cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$selector,cljs.core.filter.cljs$core$IFn$_invoke$arity$2(((function (selection_items__$1,selections,selectors,vec__66629,type,map__66630,map__66630__$1,attrs,field,id,selection_items,map__66631,map__66631__$1,opts,get){
return (function (p1__66616_SHARP_){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(p1__66616_SHARP_);
if(cljs.core.truth_(temp__4655__auto__)){
var visible_QMARK_ = temp__4655__auto__;
var G__66637 = (function (){var G__66638 = cljs.core.cst$kw$doc.cljs$core$IFn$_invoke$arity$1(opts);
return (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(G__66638) : cljs.core.deref.call(null,G__66638));
})();
return (visible_QMARK_.cljs$core$IFn$_invoke$arity$1 ? visible_QMARK_.cljs$core$IFn$_invoke$arity$1(G__66637) : visible_QMARK_.call(null,G__66637));
} else {
return true;
}
});})(selection_items__$1,selections,selectors,vec__66629,type,map__66630,map__66630__$1,attrs,field,id,selection_items,map__66631,map__66631__$1,opts,get))
,selectors)));
});
;})(selection_items__$1,selections,selectors,vec__66629,type,map__66630,map__66630__$1,attrs,field,id,selection_items,map__66631,map__66631__$1,opts,get))
});
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$single_DASH_select,(function (p__66639,p__66640){
var vec__66641 = p__66639;
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66641,(0),null);
var attrs = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66641,(1),null);
var field = vec__66641;
var map__66642 = p__66640;
var map__66642__$1 = ((((!((map__66642 == null)))?((((map__66642.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66642.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66642):map__66642);
var opts = map__66642__$1;
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66642__$1,cljs.core.cst$kw$doc);
return ((function (vec__66641,_,attrs,field,map__66642,map__66642__$1,opts,doc){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66644 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66644) : visible__66335__auto__.call(null,G__66644));
})())){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.core.selection_group,field,opts], null);
} else {
return null;
}
} else {
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.core.selection_group,field,opts], null);
}
});
;})(vec__66641,_,attrs,field,map__66642,map__66642__$1,opts,doc))
}));
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$multi_DASH_select,(function (p__66645,p__66646){
var vec__66647 = p__66645;
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66647,(0),null);
var attrs = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66647,(1),null);
var field = vec__66647;
var map__66648 = p__66646;
var map__66648__$1 = ((((!((map__66648 == null)))?((((map__66648.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66648.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66648):map__66648);
var opts = map__66648__$1;
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66648__$1,cljs.core.cst$kw$doc);
return ((function (vec__66647,_,attrs,field,map__66648,map__66648__$1,opts,doc){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66650 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66650) : visible__66335__auto__.call(null,G__66650));
})())){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.core.selection_group,field,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(opts,cljs.core.cst$kw$multi_DASH_select,true)], null);
} else {
return null;
}
} else {
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.core.selection_group,field,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(opts,cljs.core.cst$kw$multi_DASH_select,true)], null);
}
});
;})(vec__66647,_,attrs,field,map__66648,map__66648__$1,opts,doc))
}));
reagent_forms.core.map_options = (function reagent_forms$core$map_options(options){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,(function (){var iter__6925__auto__ = (function reagent_forms$core$map_options_$_iter__66669(s__66670){
return (new cljs.core.LazySeq(null,(function (){
var s__66670__$1 = s__66670;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__66670__$1);
if(temp__4657__auto__){
var s__66670__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__66670__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__66670__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__66672 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__66671 = (0);
while(true){
if((i__66671 < size__6924__auto__)){
var vec__66681 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__66671);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66681,(0),null);
var map__66682 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66681,(1),null);
var map__66682__$1 = ((((!((map__66682 == null)))?((((map__66682.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66682.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66682):map__66682);
var key = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66682__$1,cljs.core.cst$kw$key);
var label = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66681,(2),null);
cljs.core.chunk_append(b__66672,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [[cljs.core.str(label)].join(''),key], null));

var G__66687 = (i__66671 + (1));
i__66671 = G__66687;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__66672),reagent_forms$core$map_options_$_iter__66669(cljs.core.chunk_rest(s__66670__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__66672),null);
}
} else {
var vec__66684 = cljs.core.first(s__66670__$2);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66684,(0),null);
var map__66685 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66684,(1),null);
var map__66685__$1 = ((((!((map__66685 == null)))?((((map__66685.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66685.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66685):map__66685);
var key = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66685__$1,cljs.core.cst$kw$key);
var label = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66684,(2),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [[cljs.core.str(label)].join(''),key], null),reagent_forms$core$map_options_$_iter__66669(cljs.core.rest(s__66670__$2)));
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(options);
})());
});
reagent_forms.core.default_selection = (function reagent_forms$core$default_selection(options,v){
return cljs.core.last(cljs.core.first(cljs.core.filter.cljs$core$IFn$_invoke$arity$2((function (p1__66688_SHARP_){
return cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(v,cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(p1__66688_SHARP_,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(1),cljs.core.cst$kw$key], null)));
}),options)));
});
reagent_forms.core.init_field.cljs$core$IMultiFn$_add_method$arity$3(null,cljs.core.cst$kw$list,(function (p__66691,p__66692){
var vec__66693 = p__66691;
var type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66693,(0),null);
var map__66694 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__66693,(1),null);
var map__66694__$1 = ((((!((map__66694 == null)))?((((map__66694.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66694.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66694):map__66694);
var attrs = map__66694__$1;
var field = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66694__$1,cljs.core.cst$kw$field);
var id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66694__$1,cljs.core.cst$kw$id);
var options = cljs.core.nthnext(vec__66693,(2));
var map__66695 = p__66692;
var map__66695__$1 = ((((!((map__66695 == null)))?((((map__66695.cljs$lang$protocol_mask$partition0$ & (64))) || (map__66695.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__66695):map__66695);
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66695__$1,cljs.core.cst$kw$doc);
var get = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66695__$1,cljs.core.cst$kw$get);
var save_BANG_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__66695__$1,cljs.core.cst$kw$save_BANG_);
var options__$1 = reagent_forms.core.extract_selectors(options);
var options_lookup = reagent_forms.core.map_options(options__$1);
var selection = reagent.core.atom.cljs$core$IFn$_invoke$arity$1((function (){var or__6153__auto__ = (get.cljs$core$IFn$_invoke$arity$1 ? get.cljs$core$IFn$_invoke$arity$1(id) : get.call(null,id));
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(cljs.core.first(options__$1),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(1),cljs.core.cst$kw$key], null));
}
})());
var G__66698_66707 = id;
var G__66699_66708 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selection) : cljs.core.deref.call(null,selection));
(save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66698_66707,G__66699_66708) : save_BANG_.call(null,G__66698_66707,G__66699_66708));

return ((function (options__$1,options_lookup,selection,vec__66693,type,map__66694,map__66694__$1,attrs,field,id,options,map__66695,map__66695__$1,doc,get,save_BANG_){
return (function (){
var temp__4655__auto__ = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(attrs);
if(cljs.core.truth_(temp__4655__auto__)){
var visible__66335__auto__ = temp__4655__auto__;
if(cljs.core.truth_((function (){var G__66700 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible__66335__auto__.cljs$core$IFn$_invoke$arity$1 ? visible__66335__auto__.cljs$core$IFn$_invoke$arity$1(G__66700) : visible__66335__auto__.call(null,G__66700));
})())){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([attrs,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$default_DASH_value,reagent_forms.core.default_selection(options__$1,(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selection) : cljs.core.deref.call(null,selection))),cljs.core.cst$kw$on_DASH_change,((function (visible__66335__auto__,temp__4655__auto__,options__$1,options_lookup,selection,vec__66693,type,map__66694,map__66694__$1,attrs,field,id,options,map__66695,map__66695__$1,doc,get,save_BANG_){
return (function (p1__66689_SHARP_){
var G__66701 = id;
var G__66702 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(options_lookup,reagent_forms.core.value_of(p1__66689_SHARP_));
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66701,G__66702) : save_BANG_.call(null,G__66701,G__66702));
});})(visible__66335__auto__,temp__4655__auto__,options__$1,options_lookup,selection,vec__66693,type,map__66694,map__66694__$1,attrs,field,id,options,map__66695,map__66695__$1,doc,get,save_BANG_))
], null)], 0)),cljs.core.doall.cljs$core$IFn$_invoke$arity$1(cljs.core.filter.cljs$core$IFn$_invoke$arity$2(((function (visible__66335__auto__,temp__4655__auto__,options__$1,options_lookup,selection,vec__66693,type,map__66694,map__66694__$1,attrs,field,id,options,map__66695,map__66695__$1,doc,get,save_BANG_){
return (function (p1__66690_SHARP_){
var temp__4655__auto____$1 = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(cljs.core.second(p1__66690_SHARP_));
if(cljs.core.truth_(temp__4655__auto____$1)){
var visible_QMARK_ = temp__4655__auto____$1;
var G__66703 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible_QMARK_.cljs$core$IFn$_invoke$arity$1 ? visible_QMARK_.cljs$core$IFn$_invoke$arity$1(G__66703) : visible_QMARK_.call(null,G__66703));
} else {
return true;
}
});})(visible__66335__auto__,temp__4655__auto__,options__$1,options_lookup,selection,vec__66693,type,map__66694,map__66694__$1,attrs,field,id,options,map__66695,map__66695__$1,doc,get,save_BANG_))
,options__$1))], null);
} else {
return null;
}
} else {
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([attrs,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$default_DASH_value,reagent_forms.core.default_selection(options__$1,(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selection) : cljs.core.deref.call(null,selection))),cljs.core.cst$kw$on_DASH_change,((function (temp__4655__auto__,options__$1,options_lookup,selection,vec__66693,type,map__66694,map__66694__$1,attrs,field,id,options,map__66695,map__66695__$1,doc,get,save_BANG_){
return (function (p1__66689_SHARP_){
var G__66704 = id;
var G__66705 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(options_lookup,reagent_forms.core.value_of(p1__66689_SHARP_));
return (save_BANG_.cljs$core$IFn$_invoke$arity$2 ? save_BANG_.cljs$core$IFn$_invoke$arity$2(G__66704,G__66705) : save_BANG_.call(null,G__66704,G__66705));
});})(temp__4655__auto__,options__$1,options_lookup,selection,vec__66693,type,map__66694,map__66694__$1,attrs,field,id,options,map__66695,map__66695__$1,doc,get,save_BANG_))
], null)], 0)),cljs.core.doall.cljs$core$IFn$_invoke$arity$1(cljs.core.filter.cljs$core$IFn$_invoke$arity$2(((function (temp__4655__auto__,options__$1,options_lookup,selection,vec__66693,type,map__66694,map__66694__$1,attrs,field,id,options,map__66695,map__66695__$1,doc,get,save_BANG_){
return (function (p1__66690_SHARP_){
var temp__4655__auto____$1 = cljs.core.cst$kw$visible_QMARK_.cljs$core$IFn$_invoke$arity$1(cljs.core.second(p1__66690_SHARP_));
if(cljs.core.truth_(temp__4655__auto____$1)){
var visible_QMARK_ = temp__4655__auto____$1;
var G__66706 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc));
return (visible_QMARK_.cljs$core$IFn$_invoke$arity$1 ? visible_QMARK_.cljs$core$IFn$_invoke$arity$1(G__66706) : visible_QMARK_.call(null,G__66706));
} else {
return true;
}
});})(temp__4655__auto__,options__$1,options_lookup,selection,vec__66693,type,map__66694,map__66694__$1,attrs,field,id,options,map__66695,map__66695__$1,doc,get,save_BANG_))
,options__$1))], null);
}
});
;})(options__$1,options_lookup,selection,vec__66693,type,map__66694,map__66694__$1,attrs,field,id,options,map__66695,map__66695__$1,doc,get,save_BANG_))
}));
reagent_forms.core.field_QMARK_ = (function reagent_forms$core$field_QMARK_(node){
return (cljs.core.coll_QMARK_(node)) && (cljs.core.map_QMARK_(cljs.core.second(node))) && (cljs.core.contains_QMARK_(cljs.core.second(node),cljs.core.cst$kw$field));
});
/**
 * creates data bindings between the form fields and the supplied atom
 * form - the form template with the fields
 * doc - the document that the fields will be bound to
 * events - any events that should be triggered when the document state changes
 */
reagent_forms.core.bind_fields = (function reagent_forms$core$bind_fields(var_args){
var args__7218__auto__ = [];
var len__7211__auto___66713 = arguments.length;
var i__7212__auto___66714 = (0);
while(true){
if((i__7212__auto___66714 < len__7211__auto___66713)){
args__7218__auto__.push((arguments[i__7212__auto___66714]));

var G__66715 = (i__7212__auto___66714 + (1));
i__7212__auto___66714 = G__66715;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((2) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((2)),(0))):null);
return reagent_forms.core.bind_fields.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),(arguments[(1)]),argseq__7219__auto__);
});

reagent_forms.core.bind_fields.cljs$core$IFn$_invoke$arity$variadic = (function (form,doc,events){
var opts = new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$doc,doc,cljs.core.cst$kw$get,(function (p1__66709_SHARP_){
return cljs.core.get_in.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(doc) : cljs.core.deref.call(null,doc)),(reagent_forms.core.id__GT_path.cljs$core$IFn$_invoke$arity$1 ? reagent_forms.core.id__GT_path.cljs$core$IFn$_invoke$arity$1(p1__66709_SHARP_) : reagent_forms.core.id__GT_path.call(null,p1__66709_SHARP_)));
}),cljs.core.cst$kw$save_BANG_,reagent_forms.core.mk_save_fn(doc,events)], null);
var form__$1 = clojure.walk.postwalk(((function (opts){
return (function (node){
if(cljs.core.truth_(reagent_forms.core.field_QMARK_(node))){
var opts__$1 = reagent_forms.core.wrap_fns(opts,node);
var field = (reagent_forms.core.init_field.cljs$core$IFn$_invoke$arity$2 ? reagent_forms.core.init_field.cljs$core$IFn$_invoke$arity$2(node,opts__$1) : reagent_forms.core.init_field.call(null,node,opts__$1));
if(cljs.core.fn_QMARK_(field)){
return new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [field], null);
} else {
return field;
}
} else {
return node;
}
});})(opts))
,form);
return ((function (opts,form__$1){
return (function (){
return form__$1;
});
;})(opts,form__$1))
});

reagent_forms.core.bind_fields.cljs$lang$maxFixedArity = (2);

reagent_forms.core.bind_fields.cljs$lang$applyTo = (function (seq66710){
var G__66711 = cljs.core.first(seq66710);
var seq66710__$1 = cljs.core.next(seq66710);
var G__66712 = cljs.core.first(seq66710__$1);
var seq66710__$2 = cljs.core.next(seq66710__$1);
return reagent_forms.core.bind_fields.cljs$core$IFn$_invoke$arity$variadic(G__66711,G__66712,seq66710__$2);
});
