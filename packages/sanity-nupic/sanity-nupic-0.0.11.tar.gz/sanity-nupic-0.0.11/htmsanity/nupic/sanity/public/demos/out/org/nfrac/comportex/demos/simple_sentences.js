// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.demos.simple_sentences');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.core');
goog.require('org.nfrac.comportex.encoders');
goog.require('org.nfrac.comportex.util');
goog.require('clojure.string');
org.nfrac.comportex.demos.simple_sentences.bit_width = (500);
org.nfrac.comportex.demos.simple_sentences.n_on_bits = (25);
org.nfrac.comportex.demos.simple_sentences.spec = new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(1000)], null),cljs.core.cst$kw$depth,(8),cljs.core.cst$kw$distal,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$perm_DASH_init,0.21], null),cljs.core.cst$kw$distal_DASH_vs_DASH_proximal_DASH_weight,0.2], null);
org.nfrac.comportex.demos.simple_sentences.higher_level_spec = org.nfrac.comportex.util.deep_merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([org.nfrac.comportex.demos.simple_sentences.spec,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(800)], null),cljs.core.cst$kw$proximal,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$max_DASH_segments,(5)], null)], null)], 0));
org.nfrac.comportex.demos.simple_sentences.input_text = "Jane has eyes.\nJane has a head.\nJane has a mouth.\nJane has a brain.\nJane has a book.\nJane has no friend.\n\nChifung has eyes.\nChifung has a head.\nChifung has a mouth.\nChifung has a brain.\nChifung has no book.\nChifung has a friend.\n\nJane is something.\nJane is alive.\nJane is a person.\nJane can talk.\nJane can walk.\nJane can eat.\n\nChifung is something.\nChifung is alive.\nChifung is a person.\nChifung can talk.\nChifung can walk.\nChifung can eat.\n\nfox has eyes.\nfox has a head.\nfox has a mouth.\nfox has a brain.\nfox has a tail.\nfox is something.\nfox is alive.\nfox is no person.\nfox can no talk.\nfox can walk.\nfox can eat.\n\ndoes Jane have eyes ? yes.\ndoes Jane have a head ? yes.\ndoes Jane have a mouth ? yes.\ndoes Jane have a brain ? yes.\ndoes Jane have a book ? yes.\ndoes Jane have a friend ? no.\ndoes Jane have a tail ? no.\n\ndoes Chifung have eyes ? yes.\ndoes Chifung have a head ? yes.\ndoes Chifung have a mouth ? yes.\ndoes Chifung have a brain ? yes.\ndoes Chifung have a book ? no.\ndoes Chifung have a friend ? yes.\ndoes Chifung have a tail ? no.\n\ndoes fox have eyes ? yes.\ndoes fox have a head ? yes.\ndoes fox have a mouth ? yes.\ndoes fox have a brain ? yes.\ndoes fox have a book ? no.\ndoes fox have a friend ? no.\ndoes fox have a tail ? yes.\n\nJane has no tail.\nChifung has no tail.\n";
org.nfrac.comportex.demos.simple_sentences.split_sentences = (function org$nfrac$comportex$demos$simple_sentences$split_sentences(text_STAR_){
var text = clojure.string.lower_case(clojure.string.trim(text_STAR_));
return cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(((function (text){
return (function (p1__70495_SHARP_){
return cljs.core.vec(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(p1__70495_SHARP_,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, ["."], null)));
});})(text))
,cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(((function (text){
return (function (p1__70494_SHARP_){
return clojure.string.split.cljs$core$IFn$_invoke$arity$2(p1__70494_SHARP_,/[^\w']+/);
});})(text))
,clojure.string.split.cljs$core$IFn$_invoke$arity$2(text,/[^\w]*\.+[^\w]*/)));
});
/**
 * An input sequence consisting of words from the given text, with
 * periods separating sentences also included as distinct words. Each
 * sequence element has the form `{:word _, :index [i j]}`, where i is
 * the sentence index and j is the word index into sentence j.
 */
org.nfrac.comportex.demos.simple_sentences.word_item_seq = (function org$nfrac$comportex$demos$simple_sentences$word_item_seq(n_repeats,text){
var iter__6925__auto__ = (function org$nfrac$comportex$demos$simple_sentences$word_item_seq_$_iter__70533(s__70534){
return (new cljs.core.LazySeq(null,(function (){
var s__70534__$1 = s__70534;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__70534__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var vec__70556 = cljs.core.first(xs__5205__auto__);
var i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70556,(0),null);
var sen = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70556,(1),null);
var iterys__6921__auto__ = ((function (s__70534__$1,vec__70556,i,sen,xs__5205__auto__,temp__4657__auto__){
return (function org$nfrac$comportex$demos$simple_sentences$word_item_seq_$_iter__70533_$_iter__70535(s__70536){
return (new cljs.core.LazySeq(null,((function (s__70534__$1,vec__70556,i,sen,xs__5205__auto__,temp__4657__auto__){
return (function (){
var s__70536__$1 = s__70536;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__70536__$1);
if(temp__4657__auto____$1){
var xs__5205__auto____$1 = temp__4657__auto____$1;
var rep = cljs.core.first(xs__5205__auto____$1);
var iterys__6921__auto__ = ((function (s__70536__$1,s__70534__$1,rep,xs__5205__auto____$1,temp__4657__auto____$1,vec__70556,i,sen,xs__5205__auto__,temp__4657__auto__){
return (function org$nfrac$comportex$demos$simple_sentences$word_item_seq_$_iter__70533_$_iter__70535_$_iter__70537(s__70538){
return (new cljs.core.LazySeq(null,((function (s__70536__$1,s__70534__$1,rep,xs__5205__auto____$1,temp__4657__auto____$1,vec__70556,i,sen,xs__5205__auto__,temp__4657__auto__){
return (function (){
var s__70538__$1 = s__70538;
while(true){
var temp__4657__auto____$2 = cljs.core.seq(s__70538__$1);
if(temp__4657__auto____$2){
var s__70538__$2 = temp__4657__auto____$2;
if(cljs.core.chunked_seq_QMARK_(s__70538__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__70538__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__70540 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__70539 = (0);
while(true){
if((i__70539 < size__6924__auto__)){
var vec__70568 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__70539);
var j = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70568,(0),null);
var word = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70568,(1),null);
cljs.core.chunk_append(b__70540,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$word,word,cljs.core.cst$kw$index,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [i,j], null)], null));

var G__70570 = (i__70539 + (1));
i__70539 = G__70570;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__70540),org$nfrac$comportex$demos$simple_sentences$word_item_seq_$_iter__70533_$_iter__70535_$_iter__70537(cljs.core.chunk_rest(s__70538__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__70540),null);
}
} else {
var vec__70569 = cljs.core.first(s__70538__$2);
var j = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70569,(0),null);
var word = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70569,(1),null);
return cljs.core.cons(new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$word,word,cljs.core.cst$kw$index,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [i,j], null)], null),org$nfrac$comportex$demos$simple_sentences$word_item_seq_$_iter__70533_$_iter__70535_$_iter__70537(cljs.core.rest(s__70538__$2)));
}
} else {
return null;
}
break;
}
});})(s__70536__$1,s__70534__$1,rep,xs__5205__auto____$1,temp__4657__auto____$1,vec__70556,i,sen,xs__5205__auto__,temp__4657__auto__))
,null,null));
});})(s__70536__$1,s__70534__$1,rep,xs__5205__auto____$1,temp__4657__auto____$1,vec__70556,i,sen,xs__5205__auto__,temp__4657__auto__))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,sen)));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,org$nfrac$comportex$demos$simple_sentences$word_item_seq_$_iter__70533_$_iter__70535(cljs.core.rest(s__70536__$1)));
} else {
var G__70571 = cljs.core.rest(s__70536__$1);
s__70536__$1 = G__70571;
continue;
}
} else {
return null;
}
break;
}
});})(s__70534__$1,vec__70556,i,sen,xs__5205__auto__,temp__4657__auto__))
,null,null));
});})(s__70534__$1,vec__70556,i,sen,xs__5205__auto__,temp__4657__auto__))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$1(n_repeats)));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,org$nfrac$comportex$demos$simple_sentences$word_item_seq_$_iter__70533(cljs.core.rest(s__70534__$1)));
} else {
var G__70572 = cljs.core.rest(s__70534__$1);
s__70534__$1 = G__70572;
continue;
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,org.nfrac.comportex.demos.simple_sentences.split_sentences(text)));
});
org.nfrac.comportex.demos.simple_sentences.random_sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$word,org.nfrac.comportex.encoders.unique_encoder(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.simple_sentences.bit_width], null),org.nfrac.comportex.demos.simple_sentences.n_on_bits)], null);
org.nfrac.comportex.demos.simple_sentences.n_region_model = (function org$nfrac$comportex$demos$simple_sentences$n_region_model(var_args){
var args70573 = [];
var len__7211__auto___70576 = arguments.length;
var i__7212__auto___70577 = (0);
while(true){
if((i__7212__auto___70577 < len__7211__auto___70576)){
args70573.push((arguments[i__7212__auto___70577]));

var G__70578 = (i__7212__auto___70577 + (1));
i__7212__auto___70577 = G__70578;
continue;
} else {
}
break;
}

var G__70575 = args70573.length;
switch (G__70575) {
case 1:
return org.nfrac.comportex.demos.simple_sentences.n_region_model.cljs$core$IFn$_invoke$arity$1((arguments[(0)]));

break;
case 2:
return org.nfrac.comportex.demos.simple_sentences.n_region_model.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args70573.length)].join('')));

}
});

org.nfrac.comportex.demos.simple_sentences.n_region_model.cljs$core$IFn$_invoke$arity$1 = (function (n){
return org.nfrac.comportex.demos.simple_sentences.n_region_model.cljs$core$IFn$_invoke$arity$2(n,org.nfrac.comportex.demos.simple_sentences.spec);
});

org.nfrac.comportex.demos.simple_sentences.n_region_model.cljs$core$IFn$_invoke$arity$2 = (function (n,spec){
return org.nfrac.comportex.core.regions_in_series.cljs$core$IFn$_invoke$arity$4(n,org.nfrac.comportex.core.sensory_region,cljs.core.list_STAR_.cljs$core$IFn$_invoke$arity$2(spec,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.demos.simple_sentences.higher_level_spec)),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$input,org.nfrac.comportex.demos.simple_sentences.random_sensor], null));
});

org.nfrac.comportex.demos.simple_sentences.n_region_model.cljs$lang$maxFixedArity = 2;
