// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.comportex.details');
goog.require('cljs.core');
goog.require('clojure.string');
goog.require('org.nfrac.comportex.core');
goog.require('org.nfrac.comportex.protocols');
org.numenta.sanity.comportex.details.to_fixed = (function org$numenta$sanity$comportex$details$to_fixed(n,digits){
return n.toFixed(digits);
});
org.numenta.sanity.comportex.details.detail_text = (function org$numenta$sanity$comportex$details$detail_text(htm,prior_htm,rgn_id,lyr_id,col){
var rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id], null));
var lyr = cljs.core.get.cljs$core$IFn$_invoke$arity$2(rgn,lyr_id);
var depth = org.nfrac.comportex.protocols.layer_depth(lyr);
var in$ = cljs.core.cst$kw$input_DASH_value.cljs$core$IFn$_invoke$arity$1(htm);
var in_bits = cljs.core.cst$kw$in_DASH_ff_DASH_bits.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(lyr));
var in_sbits = cljs.core.cst$kw$in_DASH_stable_DASH_ff_DASH_bits.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(lyr));
return cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.str,cljs.core.interpose.cljs$core$IFn$_invoke$arity$2("\n",cljs.core.flatten(cljs.core.PersistentVector.fromArray(["__Selection__",[cljs.core.str("* timestep "),cljs.core.str(org.nfrac.comportex.protocols.timestep(rgn))].join(''),[cljs.core.str("* column "),cljs.core.str((function (){var or__6153__auto__ = col;
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return "nil";
}
})())].join(''),"","__Input__",[cljs.core.str(in$)].join(''),[cljs.core.str("("),cljs.core.str(cljs.core.count(in_bits)),cljs.core.str(" bits, of which "),cljs.core.str(cljs.core.count(in_sbits)),cljs.core.str(" stable)")].join(''),"","__Input bits__",[cljs.core.str(cljs.core.sort.cljs$core$IFn$_invoke$arity$1(in_bits))].join(''),"","__Active columns__",[cljs.core.str(cljs.core.sort.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.protocols.active_columns(lyr)))].join(''),"","__Bursting columns__",[cljs.core.str(cljs.core.sort.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.protocols.bursting_columns(lyr)))].join(''),"","__Winner cells__",[cljs.core.str(cljs.core.sort.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.protocols.winner_cells(lyr)))].join(''),"","__Proximal learning__",(function (){var iter__6925__auto__ = ((function (rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69189(s__69190){
return (new cljs.core.LazySeq(null,((function (rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69190__$1 = s__69190;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__69190__$1);
if(temp__4657__auto__){
var s__69190__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__69190__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__69190__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__69192 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__69191 = (0);
while(true){
if((i__69191 < size__6924__auto__)){
var seg_up = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__69191);
cljs.core.chunk_append(b__69192,[cljs.core.str(cljs.core.cst$kw$target_DASH_id.cljs$core$IFn$_invoke$arity$1(seg_up)),cljs.core.str(" "),cljs.core.str(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(seg_up,cljs.core.cst$kw$target_DASH_id,cljs.core.array_seq([cljs.core.cst$kw$operation], 0)))].join(''));

var G__69543 = (i__69191 + (1));
i__69191 = G__69543;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69192),org$numenta$sanity$comportex$details$detail_text_$_iter__69189(cljs.core.chunk_rest(s__69190__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69192),null);
}
} else {
var seg_up = cljs.core.first(s__69190__$2);
return cljs.core.cons([cljs.core.str(cljs.core.cst$kw$target_DASH_id.cljs$core$IFn$_invoke$arity$1(seg_up)),cljs.core.str(" "),cljs.core.str(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(seg_up,cljs.core.cst$kw$target_DASH_id,cljs.core.array_seq([cljs.core.cst$kw$operation], 0)))].join(''),org$numenta$sanity$comportex$details$detail_text_$_iter__69189(cljs.core.rest(s__69190__$2)));
}
} else {
return null;
}
break;
}
});})(rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.sort_by.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$target_DASH_id,cljs.core.vals(cljs.core.cst$kw$proximal.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$learning.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$learn_DASH_state.cljs$core$IFn$_invoke$arity$1(lyr))))));
})(),"","__Distal learning__",(function (){var iter__6925__auto__ = ((function (rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69195(s__69196){
return (new cljs.core.LazySeq(null,((function (rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69196__$1 = s__69196;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__69196__$1);
if(temp__4657__auto__){
var s__69196__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__69196__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__69196__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__69198 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__69197 = (0);
while(true){
if((i__69197 < size__6924__auto__)){
var seg_up = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__69197);
cljs.core.chunk_append(b__69198,[cljs.core.str(cljs.core.cst$kw$target_DASH_id.cljs$core$IFn$_invoke$arity$1(seg_up)),cljs.core.str(" "),cljs.core.str(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(seg_up,cljs.core.cst$kw$target_DASH_id,cljs.core.array_seq([cljs.core.cst$kw$operation], 0)))].join(''));

var G__69544 = (i__69197 + (1));
i__69197 = G__69544;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69198),org$numenta$sanity$comportex$details$detail_text_$_iter__69195(cljs.core.chunk_rest(s__69196__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69198),null);
}
} else {
var seg_up = cljs.core.first(s__69196__$2);
return cljs.core.cons([cljs.core.str(cljs.core.cst$kw$target_DASH_id.cljs$core$IFn$_invoke$arity$1(seg_up)),cljs.core.str(" "),cljs.core.str(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(seg_up,cljs.core.cst$kw$target_DASH_id,cljs.core.array_seq([cljs.core.cst$kw$operation], 0)))].join(''),org$numenta$sanity$comportex$details$detail_text_$_iter__69195(cljs.core.rest(s__69196__$2)));
}
} else {
return null;
}
break;
}
});})(rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.sort_by.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$target_DASH_id,cljs.core.vals(cljs.core.cst$kw$distal.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$learning.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$learn_DASH_state.cljs$core$IFn$_invoke$arity$1(lyr))))));
})(),"","__Distal punishments__",(function (){var iter__6925__auto__ = ((function (rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69201(s__69202){
return (new cljs.core.LazySeq(null,((function (rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69202__$1 = s__69202;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__69202__$1);
if(temp__4657__auto__){
var s__69202__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__69202__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__69202__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__69204 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__69203 = (0);
while(true){
if((i__69203 < size__6924__auto__)){
var seg_up = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__69203);
cljs.core.chunk_append(b__69204,[cljs.core.str(cljs.core.cst$kw$target_DASH_id.cljs$core$IFn$_invoke$arity$1(seg_up))].join(''));

var G__69545 = (i__69203 + (1));
i__69203 = G__69545;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69204),org$numenta$sanity$comportex$details$detail_text_$_iter__69201(cljs.core.chunk_rest(s__69202__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69204),null);
}
} else {
var seg_up = cljs.core.first(s__69202__$2);
return cljs.core.cons([cljs.core.str(cljs.core.cst$kw$target_DASH_id.cljs$core$IFn$_invoke$arity$1(seg_up))].join(''),org$numenta$sanity$comportex$details$detail_text_$_iter__69201(cljs.core.rest(s__69202__$2)));
}
} else {
return null;
}
break;
}
});})(rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.sort_by.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$target_DASH_id,cljs.core.cst$kw$distal.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$punishments.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$learn_DASH_state.cljs$core$IFn$_invoke$arity$1(lyr)))));
})(),"","__Stable cells buffer__",[cljs.core.str(cljs.core.seq(cljs.core.cst$kw$stable_DASH_cells_DASH_buffer.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(lyr))))].join(''),"",(cljs.core.truth_((function (){var and__6141__auto__ = col;
if(cljs.core.truth_(and__6141__auto__)){
return prior_htm;
} else {
return and__6141__auto__;
}
})())?(function (){var p_lyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(prior_htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id,lyr_id], null));
var p_prox_sg = cljs.core.cst$kw$proximal_DASH_sg.cljs$core$IFn$_invoke$arity$1(p_lyr);
var p_distal_sg = cljs.core.cst$kw$distal_DASH_sg.cljs$core$IFn$_invoke$arity$1(p_lyr);
var d_pcon = cljs.core.cst$kw$perm_DASH_connected.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$distal.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.protocols.params(p_lyr)));
var ff_pcon = cljs.core.cst$kw$perm_DASH_connected.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$proximal.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.protocols.params(p_lyr)));
var bits = cljs.core.cst$kw$in_DASH_ff_DASH_bits.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(lyr));
var sig_bits = cljs.core.cst$kw$in_DASH_stable_DASH_ff_DASH_bits.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(lyr));
var d_bits = cljs.core.cst$kw$active_DASH_bits.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$prior_DASH_distal_DASH_state.cljs$core$IFn$_invoke$arity$1(lyr));
var d_lbits = cljs.core.cst$kw$learnable_DASH_bits.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$prior_DASH_distal_DASH_state.cljs$core$IFn$_invoke$arity$1(lyr));
return new cljs.core.PersistentVector(null, 8, 5, cljs.core.PersistentVector.EMPTY_NODE, ["__Column overlap__",[cljs.core.str(cljs.core.get.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$col_DASH_overlaps.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(lyr)),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,(0)], null)))].join(''),"","__Selected column__","__Connected ff-synapses__",(function (){var iter__6925__auto__ = ((function (p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69207(s__69208){
return (new cljs.core.LazySeq(null,((function (p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69208__$1 = s__69208;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__69208__$1);
if(temp__4657__auto__){
var s__69208__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__69208__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__69208__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__69210 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__69209 = (0);
while(true){
if((i__69209 < size__6924__auto__)){
var vec__69243 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__69209);
var si = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69243,(0),null);
var syns = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69243,(1),null);
if(cljs.core.seq(syns)){
cljs.core.chunk_append(b__69210,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [[cljs.core.str("FF segment "),cljs.core.str(si)].join(''),(function (){var iter__6925__auto__ = ((function (i__69209,s__69208__$1,vec__69243,si,syns,c__6923__auto__,size__6924__auto__,b__69210,s__69208__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69207_$_iter__69244(s__69245){
return (new cljs.core.LazySeq(null,((function (i__69209,s__69208__$1,vec__69243,si,syns,c__6923__auto__,size__6924__auto__,b__69210,s__69208__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69245__$1 = s__69245;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__69245__$1);
if(temp__4657__auto____$1){
var s__69245__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__69245__$2)){
var c__6923__auto____$1 = cljs.core.chunk_first(s__69245__$2);
var size__6924__auto____$1 = cljs.core.count(c__6923__auto____$1);
var b__69247 = cljs.core.chunk_buffer(size__6924__auto____$1);
if((function (){var i__69246 = (0);
while(true){
if((i__69246 < size__6924__auto____$1)){
var vec__69254 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto____$1,i__69246);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69254,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69254,(1),null);
var vec__69255 = org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$4(htm,rgn_id,id,cljs.core.cst$kw$ff_DASH_deps);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69255,(0),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69255,(1),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
cljs.core.chunk_append(b__69247,[cljs.core.str("  "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= ff_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(sig_bits,id))?" S":((cljs.core.contains_QMARK_(bits,id))?" A":null)))].join(''));

var G__69546 = (i__69246 + (1));
i__69246 = G__69546;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69247),org$numenta$sanity$comportex$details$detail_text_$_iter__69207_$_iter__69244(cljs.core.chunk_rest(s__69245__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69247),null);
}
} else {
var vec__69256 = cljs.core.first(s__69245__$2);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69256,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69256,(1),null);
var vec__69257 = org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$4(htm,rgn_id,id,cljs.core.cst$kw$ff_DASH_deps);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69257,(0),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69257,(1),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
return cljs.core.cons([cljs.core.str("  "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= ff_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(sig_bits,id))?" S":((cljs.core.contains_QMARK_(bits,id))?" A":null)))].join(''),org$numenta$sanity$comportex$details$detail_text_$_iter__69207_$_iter__69244(cljs.core.rest(s__69245__$2)));
}
} else {
return null;
}
break;
}
});})(i__69209,s__69208__$1,vec__69243,si,syns,c__6923__auto__,size__6924__auto__,b__69210,s__69208__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(i__69209,s__69208__$1,vec__69243,si,syns,c__6923__auto__,size__6924__auto__,b__69210,s__69208__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.sort.cljs$core$IFn$_invoke$arity$1(syns));
})()], null));

var G__69547 = (i__69209 + (1));
i__69209 = G__69547;
continue;
} else {
var G__69548 = (i__69209 + (1));
i__69209 = G__69548;
continue;
}
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69210),org$numenta$sanity$comportex$details$detail_text_$_iter__69207(cljs.core.chunk_rest(s__69208__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69210),null);
}
} else {
var vec__69258 = cljs.core.first(s__69208__$2);
var si = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69258,(0),null);
var syns = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69258,(1),null);
if(cljs.core.seq(syns)){
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [[cljs.core.str("FF segment "),cljs.core.str(si)].join(''),(function (){var iter__6925__auto__ = ((function (s__69208__$1,vec__69258,si,syns,s__69208__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69207_$_iter__69259(s__69260){
return (new cljs.core.LazySeq(null,((function (s__69208__$1,vec__69258,si,syns,s__69208__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69260__$1 = s__69260;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__69260__$1);
if(temp__4657__auto____$1){
var s__69260__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__69260__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__69260__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__69262 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__69261 = (0);
while(true){
if((i__69261 < size__6924__auto__)){
var vec__69269 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__69261);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69269,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69269,(1),null);
var vec__69270 = org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$4(htm,rgn_id,id,cljs.core.cst$kw$ff_DASH_deps);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69270,(0),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69270,(1),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
cljs.core.chunk_append(b__69262,[cljs.core.str("  "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= ff_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(sig_bits,id))?" S":((cljs.core.contains_QMARK_(bits,id))?" A":null)))].join(''));

var G__69549 = (i__69261 + (1));
i__69261 = G__69549;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69262),org$numenta$sanity$comportex$details$detail_text_$_iter__69207_$_iter__69259(cljs.core.chunk_rest(s__69260__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69262),null);
}
} else {
var vec__69271 = cljs.core.first(s__69260__$2);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69271,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69271,(1),null);
var vec__69272 = org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$4(htm,rgn_id,id,cljs.core.cst$kw$ff_DASH_deps);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69272,(0),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69272,(1),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
return cljs.core.cons([cljs.core.str("  "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= ff_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(sig_bits,id))?" S":((cljs.core.contains_QMARK_(bits,id))?" A":null)))].join(''),org$numenta$sanity$comportex$details$detail_text_$_iter__69207_$_iter__69259(cljs.core.rest(s__69260__$2)));
}
} else {
return null;
}
break;
}
});})(s__69208__$1,vec__69258,si,syns,s__69208__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(s__69208__$1,vec__69258,si,syns,s__69208__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.sort.cljs$core$IFn$_invoke$arity$1(syns));
})()], null),org$numenta$sanity$comportex$details$detail_text_$_iter__69207(cljs.core.rest(s__69208__$2)));
} else {
var G__69550 = cljs.core.rest(s__69208__$2);
s__69208__$1 = G__69550;
continue;
}
}
} else {
return null;
}
break;
}
});})(p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,org.nfrac.comportex.protocols.cell_segments(p_prox_sg,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,(0)], null))));
})(),"__Cells and their distal dendrite segments__",(function (){var iter__6925__auto__ = ((function (p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69273(s__69274){
return (new cljs.core.LazySeq(null,((function (p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69274__$1 = s__69274;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__69274__$1);
if(temp__4657__auto__){
var s__69274__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__69274__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__69274__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__69276 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__69275 = (0);
while(true){
if((i__69275 < size__6924__auto__)){
var ci = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__69275);
var segs = org.nfrac.comportex.protocols.cell_segments(p_distal_sg,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,ci], null));
cljs.core.chunk_append(b__69276,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [[cljs.core.str("CELL "),cljs.core.str(ci)].join(''),[cljs.core.str(cljs.core.count(segs)),cljs.core.str(" = "),cljs.core.str(cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.count,segs))].join(''),(function (){var iter__6925__auto__ = ((function (i__69275,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69411(s__69412){
return (new cljs.core.LazySeq(null,((function (i__69275,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69412__$1 = s__69412;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__69412__$1);
if(temp__4657__auto____$1){
var s__69412__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__69412__$2)){
var c__6923__auto____$1 = cljs.core.chunk_first(s__69412__$2);
var size__6924__auto____$1 = cljs.core.count(c__6923__auto____$1);
var b__69414 = cljs.core.chunk_buffer(size__6924__auto____$1);
if((function (){var i__69413 = (0);
while(true){
if((i__69413 < size__6924__auto____$1)){
var vec__69447 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto____$1,i__69413);
var si = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69447,(0),null);
var syns = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69447,(1),null);
cljs.core.chunk_append(b__69414,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [[cljs.core.str("  SEGMENT "),cljs.core.str(si)].join(''),(function (){var iter__6925__auto__ = ((function (i__69413,i__69275,vec__69447,si,syns,c__6923__auto____$1,size__6924__auto____$1,b__69414,s__69412__$2,temp__4657__auto____$1,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69411_$_iter__69448(s__69449){
return (new cljs.core.LazySeq(null,((function (i__69413,i__69275,vec__69447,si,syns,c__6923__auto____$1,size__6924__auto____$1,b__69414,s__69412__$2,temp__4657__auto____$1,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69449__$1 = s__69449;
while(true){
var temp__4657__auto____$2 = cljs.core.seq(s__69449__$1);
if(temp__4657__auto____$2){
var s__69449__$2 = temp__4657__auto____$2;
if(cljs.core.chunked_seq_QMARK_(s__69449__$2)){
var c__6923__auto____$2 = cljs.core.chunk_first(s__69449__$2);
var size__6924__auto____$2 = cljs.core.count(c__6923__auto____$2);
var b__69451 = cljs.core.chunk_buffer(size__6924__auto____$2);
if((function (){var i__69450 = (0);
while(true){
if((i__69450 < size__6924__auto____$2)){
var vec__69458 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto____$2,i__69450);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69458,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69458,(1),null);
var vec__69459 = org.nfrac.comportex.core.source_of_distal_bit(htm,rgn_id,lyr_id,id);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69459,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69459,(1),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69459,(2),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
cljs.core.chunk_append(b__69451,[cljs.core.str("    "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= d_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(d_lbits,id))?" L":((cljs.core.contains_QMARK_(d_bits,id))?" A":null)))].join(''));

var G__69551 = (i__69450 + (1));
i__69450 = G__69551;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69451),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69411_$_iter__69448(cljs.core.chunk_rest(s__69449__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69451),null);
}
} else {
var vec__69460 = cljs.core.first(s__69449__$2);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69460,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69460,(1),null);
var vec__69461 = org.nfrac.comportex.core.source_of_distal_bit(htm,rgn_id,lyr_id,id);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69461,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69461,(1),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69461,(2),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
return cljs.core.cons([cljs.core.str("    "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= d_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(d_lbits,id))?" L":((cljs.core.contains_QMARK_(d_bits,id))?" A":null)))].join(''),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69411_$_iter__69448(cljs.core.rest(s__69449__$2)));
}
} else {
return null;
}
break;
}
});})(i__69413,i__69275,vec__69447,si,syns,c__6923__auto____$1,size__6924__auto____$1,b__69414,s__69412__$2,temp__4657__auto____$1,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(i__69413,i__69275,vec__69447,si,syns,c__6923__auto____$1,size__6924__auto____$1,b__69414,s__69412__$2,temp__4657__auto____$1,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.sort.cljs$core$IFn$_invoke$arity$1(syns));
})()], null));

var G__69552 = (i__69413 + (1));
i__69413 = G__69552;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69414),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69411(cljs.core.chunk_rest(s__69412__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69414),null);
}
} else {
var vec__69462 = cljs.core.first(s__69412__$2);
var si = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69462,(0),null);
var syns = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69462,(1),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [[cljs.core.str("  SEGMENT "),cljs.core.str(si)].join(''),(function (){var iter__6925__auto__ = ((function (i__69275,vec__69462,si,syns,s__69412__$2,temp__4657__auto____$1,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69411_$_iter__69463(s__69464){
return (new cljs.core.LazySeq(null,((function (i__69275,vec__69462,si,syns,s__69412__$2,temp__4657__auto____$1,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69464__$1 = s__69464;
while(true){
var temp__4657__auto____$2 = cljs.core.seq(s__69464__$1);
if(temp__4657__auto____$2){
var s__69464__$2 = temp__4657__auto____$2;
if(cljs.core.chunked_seq_QMARK_(s__69464__$2)){
var c__6923__auto____$1 = cljs.core.chunk_first(s__69464__$2);
var size__6924__auto____$1 = cljs.core.count(c__6923__auto____$1);
var b__69466 = cljs.core.chunk_buffer(size__6924__auto____$1);
if((function (){var i__69465 = (0);
while(true){
if((i__69465 < size__6924__auto____$1)){
var vec__69473 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto____$1,i__69465);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69473,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69473,(1),null);
var vec__69474 = org.nfrac.comportex.core.source_of_distal_bit(htm,rgn_id,lyr_id,id);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69474,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69474,(1),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69474,(2),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
cljs.core.chunk_append(b__69466,[cljs.core.str("    "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= d_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(d_lbits,id))?" L":((cljs.core.contains_QMARK_(d_bits,id))?" A":null)))].join(''));

var G__69553 = (i__69465 + (1));
i__69465 = G__69553;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69466),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69411_$_iter__69463(cljs.core.chunk_rest(s__69464__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69466),null);
}
} else {
var vec__69475 = cljs.core.first(s__69464__$2);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69475,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69475,(1),null);
var vec__69476 = org.nfrac.comportex.core.source_of_distal_bit(htm,rgn_id,lyr_id,id);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69476,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69476,(1),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69476,(2),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
return cljs.core.cons([cljs.core.str("    "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= d_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(d_lbits,id))?" L":((cljs.core.contains_QMARK_(d_bits,id))?" A":null)))].join(''),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69411_$_iter__69463(cljs.core.rest(s__69464__$2)));
}
} else {
return null;
}
break;
}
});})(i__69275,vec__69462,si,syns,s__69412__$2,temp__4657__auto____$1,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(i__69275,vec__69462,si,syns,s__69412__$2,temp__4657__auto____$1,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.sort.cljs$core$IFn$_invoke$arity$1(syns));
})()], null),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69411(cljs.core.rest(s__69412__$2)));
}
} else {
return null;
}
break;
}
});})(i__69275,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(i__69275,segs,ci,c__6923__auto__,size__6924__auto__,b__69276,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,segs));
})()], null));

var G__69554 = (i__69275 + (1));
i__69275 = G__69554;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69276),org$numenta$sanity$comportex$details$detail_text_$_iter__69273(cljs.core.chunk_rest(s__69274__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69276),null);
}
} else {
var ci = cljs.core.first(s__69274__$2);
var segs = org.nfrac.comportex.protocols.cell_segments(p_distal_sg,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,ci], null));
return cljs.core.cons(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [[cljs.core.str("CELL "),cljs.core.str(ci)].join(''),[cljs.core.str(cljs.core.count(segs)),cljs.core.str(" = "),cljs.core.str(cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.count,segs))].join(''),(function (){var iter__6925__auto__ = ((function (segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69477(s__69478){
return (new cljs.core.LazySeq(null,((function (segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69478__$1 = s__69478;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__69478__$1);
if(temp__4657__auto____$1){
var s__69478__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__69478__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__69478__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__69480 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__69479 = (0);
while(true){
if((i__69479 < size__6924__auto__)){
var vec__69513 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__69479);
var si = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69513,(0),null);
var syns = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69513,(1),null);
cljs.core.chunk_append(b__69480,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [[cljs.core.str("  SEGMENT "),cljs.core.str(si)].join(''),(function (){var iter__6925__auto__ = ((function (i__69479,vec__69513,si,syns,c__6923__auto__,size__6924__auto__,b__69480,s__69478__$2,temp__4657__auto____$1,segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69477_$_iter__69514(s__69515){
return (new cljs.core.LazySeq(null,((function (i__69479,vec__69513,si,syns,c__6923__auto__,size__6924__auto__,b__69480,s__69478__$2,temp__4657__auto____$1,segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69515__$1 = s__69515;
while(true){
var temp__4657__auto____$2 = cljs.core.seq(s__69515__$1);
if(temp__4657__auto____$2){
var s__69515__$2 = temp__4657__auto____$2;
if(cljs.core.chunked_seq_QMARK_(s__69515__$2)){
var c__6923__auto____$1 = cljs.core.chunk_first(s__69515__$2);
var size__6924__auto____$1 = cljs.core.count(c__6923__auto____$1);
var b__69517 = cljs.core.chunk_buffer(size__6924__auto____$1);
if((function (){var i__69516 = (0);
while(true){
if((i__69516 < size__6924__auto____$1)){
var vec__69524 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto____$1,i__69516);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69524,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69524,(1),null);
var vec__69525 = org.nfrac.comportex.core.source_of_distal_bit(htm,rgn_id,lyr_id,id);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69525,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69525,(1),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69525,(2),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
cljs.core.chunk_append(b__69517,[cljs.core.str("    "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= d_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(d_lbits,id))?" L":((cljs.core.contains_QMARK_(d_bits,id))?" A":null)))].join(''));

var G__69555 = (i__69516 + (1));
i__69516 = G__69555;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69517),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69477_$_iter__69514(cljs.core.chunk_rest(s__69515__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69517),null);
}
} else {
var vec__69526 = cljs.core.first(s__69515__$2);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69526,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69526,(1),null);
var vec__69527 = org.nfrac.comportex.core.source_of_distal_bit(htm,rgn_id,lyr_id,id);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69527,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69527,(1),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69527,(2),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
return cljs.core.cons([cljs.core.str("    "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= d_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(d_lbits,id))?" L":((cljs.core.contains_QMARK_(d_bits,id))?" A":null)))].join(''),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69477_$_iter__69514(cljs.core.rest(s__69515__$2)));
}
} else {
return null;
}
break;
}
});})(i__69479,vec__69513,si,syns,c__6923__auto__,size__6924__auto__,b__69480,s__69478__$2,temp__4657__auto____$1,segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(i__69479,vec__69513,si,syns,c__6923__auto__,size__6924__auto__,b__69480,s__69478__$2,temp__4657__auto____$1,segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.sort.cljs$core$IFn$_invoke$arity$1(syns));
})()], null));

var G__69556 = (i__69479 + (1));
i__69479 = G__69556;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69480),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69477(cljs.core.chunk_rest(s__69478__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69480),null);
}
} else {
var vec__69528 = cljs.core.first(s__69478__$2);
var si = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69528,(0),null);
var syns = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69528,(1),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [[cljs.core.str("  SEGMENT "),cljs.core.str(si)].join(''),(function (){var iter__6925__auto__ = ((function (vec__69528,si,syns,s__69478__$2,temp__4657__auto____$1,segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69477_$_iter__69529(s__69530){
return (new cljs.core.LazySeq(null,((function (vec__69528,si,syns,s__69478__$2,temp__4657__auto____$1,segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits){
return (function (){
var s__69530__$1 = s__69530;
while(true){
var temp__4657__auto____$2 = cljs.core.seq(s__69530__$1);
if(temp__4657__auto____$2){
var s__69530__$2 = temp__4657__auto____$2;
if(cljs.core.chunked_seq_QMARK_(s__69530__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__69530__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__69532 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__69531 = (0);
while(true){
if((i__69531 < size__6924__auto__)){
var vec__69539 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__69531);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69539,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69539,(1),null);
var vec__69540 = org.nfrac.comportex.core.source_of_distal_bit(htm,rgn_id,lyr_id,id);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69540,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69540,(1),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69540,(2),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
cljs.core.chunk_append(b__69532,[cljs.core.str("    "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= d_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(d_lbits,id))?" L":((cljs.core.contains_QMARK_(d_bits,id))?" A":null)))].join(''));

var G__69557 = (i__69531 + (1));
i__69531 = G__69557;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69532),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69477_$_iter__69529(cljs.core.chunk_rest(s__69530__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69532),null);
}
} else {
var vec__69541 = cljs.core.first(s__69530__$2);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69541,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69541,(1),null);
var vec__69542 = org.nfrac.comportex.core.source_of_distal_bit(htm,rgn_id,lyr_id,id);
var src_k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69542,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69542,(1),null);
var src_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69542,(2),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_k], null));
var src_id = (cljs.core.truth_(src_rgn)?org.nfrac.comportex.protocols.source_of_bit(src_rgn,src_i):src_i);
return cljs.core.cons([cljs.core.str("    "),cljs.core.str(src_k),cljs.core.str(" "),cljs.core.str(src_id),cljs.core.str((((p >= d_pcon))?" :=> ":" :.: ")),cljs.core.str(org.numenta.sanity.comportex.details.to_fixed(p,(2))),cljs.core.str(((cljs.core.contains_QMARK_(d_lbits,id))?" L":((cljs.core.contains_QMARK_(d_bits,id))?" A":null)))].join(''),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69477_$_iter__69529(cljs.core.rest(s__69530__$2)));
}
} else {
return null;
}
break;
}
});})(vec__69528,si,syns,s__69478__$2,temp__4657__auto____$1,segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(vec__69528,si,syns,s__69478__$2,temp__4657__auto____$1,segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.sort.cljs$core$IFn$_invoke$arity$1(syns));
})()], null),org$numenta$sanity$comportex$details$detail_text_$_iter__69273_$_iter__69477(cljs.core.rest(s__69478__$2)));
}
} else {
return null;
}
break;
}
});})(segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(segs,ci,s__69274__$2,temp__4657__auto__,p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,segs));
})()], null),org$numenta$sanity$comportex$details$detail_text_$_iter__69273(cljs.core.rest(s__69274__$2)));
}
} else {
return null;
}
break;
}
});})(p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
,null,null));
});})(p_lyr,p_prox_sg,p_distal_sg,d_pcon,ff_pcon,bits,sig_bits,d_bits,d_lbits,rgn,lyr,depth,in$,in_bits,in_sbits))
;
return iter__6925__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.protocols.layer_depth(lyr)));
})()], null);
})():null),"","__spec__",cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.str,cljs.core.sort.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.protocols.params(rgn)))], true))));
});
