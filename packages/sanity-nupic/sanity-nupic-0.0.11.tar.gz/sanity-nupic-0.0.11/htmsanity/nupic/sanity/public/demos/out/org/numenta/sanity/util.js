// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.util');
goog.require('cljs.core');
goog.require('cljs.core.async');
goog.require('clojure.walk');
org.numenta.sanity.util.tap_c = (function org$numenta$sanity$util$tap_c(mult){
var c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
cljs.core.async.tap.cljs$core$IFn$_invoke$arity$2(mult,c);

return c;
});
org.numenta.sanity.util.index_of = (function org$numenta$sanity$util$index_of(coll,pred){
return cljs.core.first(cljs.core.keep_indexed.cljs$core$IFn$_invoke$arity$2((function (i,v){
if(cljs.core.truth_((pred.cljs$core$IFn$_invoke$arity$1 ? pred.cljs$core$IFn$_invoke$arity$1(v) : pred.call(null,v)))){
return i;
} else {
return null;
}
}),coll));
});
org.numenta.sanity.util.translate_network_shape = (function org$numenta$sanity$util$translate_network_shape(n_shape_from_server){
var map__45518 = n_shape_from_server;
var map__45518__$1 = ((((!((map__45518 == null)))?((((map__45518.cljs$lang$protocol_mask$partition0$ & (64))) || (map__45518.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__45518):map__45518);
var regions = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__45518__$1,"regions");
var senses = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__45518__$1,"senses");
return new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$regions,cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,(function (){var iter__6925__auto__ = ((function (map__45518,map__45518__$1,regions,senses){
return (function org$numenta$sanity$util$translate_network_shape_$_iter__45520(s__45521){
return (new cljs.core.LazySeq(null,((function (map__45518,map__45518__$1,regions,senses){
return (function (){
var s__45521__$1 = s__45521;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__45521__$1);
if(temp__4657__auto__){
var s__45521__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__45521__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__45521__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__45523 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__45522 = (0);
while(true){
if((i__45522 < size__6924__auto__)){
var vec__45548 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__45522);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45548,(0),null);
var rgn = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45548,(1),null);
cljs.core.chunk_append(b__45523,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [rgn_id,cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,(function (){var iter__6925__auto__ = ((function (i__45522,vec__45548,rgn_id,rgn,c__6923__auto__,size__6924__auto__,b__45523,s__45521__$2,temp__4657__auto__,map__45518,map__45518__$1,regions,senses){
return (function org$numenta$sanity$util$translate_network_shape_$_iter__45520_$_iter__45549(s__45550){
return (new cljs.core.LazySeq(null,((function (i__45522,vec__45548,rgn_id,rgn,c__6923__auto__,size__6924__auto__,b__45523,s__45521__$2,temp__4657__auto__,map__45518,map__45518__$1,regions,senses){
return (function (){
var s__45550__$1 = s__45550;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__45550__$1);
if(temp__4657__auto____$1){
var s__45550__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__45550__$2)){
var c__6923__auto____$1 = cljs.core.chunk_first(s__45550__$2);
var size__6924__auto____$1 = cljs.core.count(c__6923__auto____$1);
var b__45552 = cljs.core.chunk_buffer(size__6924__auto____$1);
if((function (){var i__45551 = (0);
while(true){
if((i__45551 < size__6924__auto____$1)){
var vec__45557 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto____$1,i__45551);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45557,(0),null);
var lyr = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45557,(1),null);
cljs.core.chunk_append(b__45552,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [lyr_id,clojure.walk.keywordize_keys(lyr)], null));

var G__45580 = (i__45551 + (1));
i__45551 = G__45580;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__45552),org$numenta$sanity$util$translate_network_shape_$_iter__45520_$_iter__45549(cljs.core.chunk_rest(s__45550__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__45552),null);
}
} else {
var vec__45558 = cljs.core.first(s__45550__$2);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45558,(0),null);
var lyr = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45558,(1),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [lyr_id,clojure.walk.keywordize_keys(lyr)], null),org$numenta$sanity$util$translate_network_shape_$_iter__45520_$_iter__45549(cljs.core.rest(s__45550__$2)));
}
} else {
return null;
}
break;
}
});})(i__45522,vec__45548,rgn_id,rgn,c__6923__auto__,size__6924__auto__,b__45523,s__45521__$2,temp__4657__auto__,map__45518,map__45518__$1,regions,senses))
,null,null));
});})(i__45522,vec__45548,rgn_id,rgn,c__6923__auto__,size__6924__auto__,b__45523,s__45521__$2,temp__4657__auto__,map__45518,map__45518__$1,regions,senses))
;
return iter__6925__auto__(rgn);
})())], null));

var G__45581 = (i__45522 + (1));
i__45522 = G__45581;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__45523),org$numenta$sanity$util$translate_network_shape_$_iter__45520(cljs.core.chunk_rest(s__45521__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__45523),null);
}
} else {
var vec__45559 = cljs.core.first(s__45521__$2);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45559,(0),null);
var rgn = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45559,(1),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [rgn_id,cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,(function (){var iter__6925__auto__ = ((function (vec__45559,rgn_id,rgn,s__45521__$2,temp__4657__auto__,map__45518,map__45518__$1,regions,senses){
return (function org$numenta$sanity$util$translate_network_shape_$_iter__45520_$_iter__45560(s__45561){
return (new cljs.core.LazySeq(null,((function (vec__45559,rgn_id,rgn,s__45521__$2,temp__4657__auto__,map__45518,map__45518__$1,regions,senses){
return (function (){
var s__45561__$1 = s__45561;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__45561__$1);
if(temp__4657__auto____$1){
var s__45561__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__45561__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__45561__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__45563 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__45562 = (0);
while(true){
if((i__45562 < size__6924__auto__)){
var vec__45568 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__45562);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45568,(0),null);
var lyr = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45568,(1),null);
cljs.core.chunk_append(b__45563,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [lyr_id,clojure.walk.keywordize_keys(lyr)], null));

var G__45582 = (i__45562 + (1));
i__45562 = G__45582;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__45563),org$numenta$sanity$util$translate_network_shape_$_iter__45520_$_iter__45560(cljs.core.chunk_rest(s__45561__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__45563),null);
}
} else {
var vec__45569 = cljs.core.first(s__45561__$2);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45569,(0),null);
var lyr = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45569,(1),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [lyr_id,clojure.walk.keywordize_keys(lyr)], null),org$numenta$sanity$util$translate_network_shape_$_iter__45520_$_iter__45560(cljs.core.rest(s__45561__$2)));
}
} else {
return null;
}
break;
}
});})(vec__45559,rgn_id,rgn,s__45521__$2,temp__4657__auto__,map__45518,map__45518__$1,regions,senses))
,null,null));
});})(vec__45559,rgn_id,rgn,s__45521__$2,temp__4657__auto__,map__45518,map__45518__$1,regions,senses))
;
return iter__6925__auto__(rgn);
})())], null),org$numenta$sanity$util$translate_network_shape_$_iter__45520(cljs.core.rest(s__45521__$2)));
}
} else {
return null;
}
break;
}
});})(map__45518,map__45518__$1,regions,senses))
,null,null));
});})(map__45518,map__45518__$1,regions,senses))
;
return iter__6925__auto__(regions);
})()),cljs.core.cst$kw$senses,cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,(function (){var iter__6925__auto__ = ((function (map__45518,map__45518__$1,regions,senses){
return (function org$numenta$sanity$util$translate_network_shape_$_iter__45570(s__45571){
return (new cljs.core.LazySeq(null,((function (map__45518,map__45518__$1,regions,senses){
return (function (){
var s__45571__$1 = s__45571;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__45571__$1);
if(temp__4657__auto__){
var s__45571__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__45571__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__45571__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__45573 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__45572 = (0);
while(true){
if((i__45572 < size__6924__auto__)){
var vec__45578 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__45572);
var sense_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45578,(0),null);
var sense = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45578,(1),null);
cljs.core.chunk_append(b__45573,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [sense_id,clojure.walk.keywordize_keys(sense)], null));

var G__45583 = (i__45572 + (1));
i__45572 = G__45583;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__45573),org$numenta$sanity$util$translate_network_shape_$_iter__45570(cljs.core.chunk_rest(s__45571__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__45573),null);
}
} else {
var vec__45579 = cljs.core.first(s__45571__$2);
var sense_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45579,(0),null);
var sense = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__45579,(1),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [sense_id,clojure.walk.keywordize_keys(sense)], null),org$numenta$sanity$util$translate_network_shape_$_iter__45570(cljs.core.rest(s__45571__$2)));
}
} else {
return null;
}
break;
}
});})(map__45518,map__45518__$1,regions,senses))
,null,null));
});})(map__45518,map__45518__$1,regions,senses))
;
return iter__6925__auto__(senses);
})())], null);
});
