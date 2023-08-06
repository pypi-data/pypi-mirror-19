// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.topology');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.protocols');
org.nfrac.comportex.topology.abs = (function org$nfrac$comportex$topology$abs(x){
if((x < (0))){
return (- x);
} else {
return x;
}
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {org.nfrac.comportex.protocols.PTopology}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.nfrac.comportex.topology.OneDTopology = (function (size,__meta,__extmap,__hash){
this.size = size;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k36510,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__36512 = (((k36510 instanceof cljs.core.Keyword))?k36510.fqn:null);
switch (G__36512) {
case "size":
return self__.size;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k36510,else__6770__auto__);

}
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.nfrac.comportex.topology.OneDTopology{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$size,self__.size],null))], null),self__.__extmap));
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$IIterable$ = true;

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__36509){
var self__ = this;
var G__36509__$1 = this;
return (new cljs.core.RecordIter((0),G__36509__$1,1,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$size], null),cljs.core._iterator(self__.__extmap)));
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.nfrac.comportex.topology.OneDTopology(self__.size,self__.__meta,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (1 + cljs.core.count(self__.__extmap));
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
var self__ = this;
var this__6762__auto____$1 = this;
var h__6588__auto__ = self__.__hash;
if(!((h__6588__auto__ == null))){
return h__6588__auto__;
} else {
var h__6588__auto____$1 = cljs.core.hash_imap(this__6762__auto____$1);
self__.__hash = h__6588__auto____$1;

return h__6588__auto____$1;
}
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
var self__ = this;
var this__6763__auto____$1 = this;
if(cljs.core.truth_((function (){var and__6141__auto__ = other__6764__auto__;
if(cljs.core.truth_(and__6141__auto__)){
var and__6141__auto____$1 = (this__6763__auto____$1.constructor === other__6764__auto__.constructor);
if(and__6141__auto____$1){
return cljs.core.equiv_map(this__6763__auto____$1,other__6764__auto__);
} else {
return and__6141__auto____$1;
}
} else {
return and__6141__auto__;
}
})())){
return true;
} else {
return false;
}
});

org.nfrac.comportex.topology.OneDTopology.prototype.org$nfrac$comportex$protocols$PTopology$ = true;

org.nfrac.comportex.topology.OneDTopology.prototype.org$nfrac$comportex$protocols$PTopology$dimensions$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [self__.size], null);
});

org.nfrac.comportex.topology.OneDTopology.prototype.org$nfrac$comportex$protocols$PTopology$coordinates_of_index$arity$2 = (function (_,idx){
var self__ = this;
var ___$1 = this;
return idx;
});

org.nfrac.comportex.topology.OneDTopology.prototype.org$nfrac$comportex$protocols$PTopology$index_of_coordinates$arity$2 = (function (_,coord){
var self__ = this;
var ___$1 = this;
return coord;
});

org.nfrac.comportex.topology.OneDTopology.prototype.org$nfrac$comportex$protocols$PTopology$neighbours_STAR_$arity$4 = (function (this$,coord,outer_r,inner_r){
var self__ = this;
var this$__$1 = this;
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(cljs.core.range.cljs$core$IFn$_invoke$arity$2((function (){var x__6491__auto__ = ((coord + inner_r) + (1));
var y__6492__auto__ = self__.size;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})(),(function (){var x__6491__auto__ = ((coord + outer_r) + (1));
var y__6492__auto__ = self__.size;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})()),cljs.core.range.cljs$core$IFn$_invoke$arity$2((function (){var x__6484__auto__ = (coord - outer_r);
var y__6485__auto__ = (0);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})(),(function (){var x__6484__auto__ = (coord - inner_r);
var y__6485__auto__ = (0);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})()));
});

org.nfrac.comportex.topology.OneDTopology.prototype.org$nfrac$comportex$protocols$PTopology$coord_distance$arity$3 = (function (_,coord_a,coord_b){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.topology.abs((coord_b - coord_a));
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$size,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.nfrac.comportex.topology.OneDTopology(self__.size,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__36509){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__36513 = cljs.core.keyword_identical_QMARK_;
var expr__36514 = k__6775__auto__;
if(cljs.core.truth_((pred__36513.cljs$core$IFn$_invoke$arity$2 ? pred__36513.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$size,expr__36514) : pred__36513.call(null,cljs.core.cst$kw$size,expr__36514)))){
return (new org.nfrac.comportex.topology.OneDTopology(G__36509,self__.__meta,self__.__extmap,null));
} else {
return (new org.nfrac.comportex.topology.OneDTopology(self__.size,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__36509),null));
}
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$size,self__.size],null))], null),self__.__extmap));
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__36509){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.nfrac.comportex.topology.OneDTopology(self__.size,G__36509,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.topology.OneDTopology.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.nfrac.comportex.topology.OneDTopology.getBasis = (function (){
return new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$size], null);
});

org.nfrac.comportex.topology.OneDTopology.cljs$lang$type = true;

org.nfrac.comportex.topology.OneDTopology.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.nfrac.comportex.topology/OneDTopology");
});

org.nfrac.comportex.topology.OneDTopology.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.nfrac.comportex.topology/OneDTopology");
});

org.nfrac.comportex.topology.__GT_OneDTopology = (function org$nfrac$comportex$topology$__GT_OneDTopology(size){
return (new org.nfrac.comportex.topology.OneDTopology(size,null,null,null));
});

org.nfrac.comportex.topology.map__GT_OneDTopology = (function org$nfrac$comportex$topology$map__GT_OneDTopology(G__36511){
return (new org.nfrac.comportex.topology.OneDTopology(cljs.core.cst$kw$size.cljs$core$IFn$_invoke$arity$1(G__36511),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(G__36511,cljs.core.cst$kw$size),null));
});

org.nfrac.comportex.topology.one_d_topology = (function org$nfrac$comportex$topology$one_d_topology(size){
return org.nfrac.comportex.topology.__GT_OneDTopology(size);
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {org.nfrac.comportex.protocols.PTopology}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.nfrac.comportex.topology.TwoDTopology = (function (width,height,__meta,__extmap,__hash){
this.width = width;
this.height = height;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k36518,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__36520 = (((k36518 instanceof cljs.core.Keyword))?k36518.fqn:null);
switch (G__36520) {
case "width":
return self__.width;

break;
case "height":
return self__.height;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k36518,else__6770__auto__);

}
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.nfrac.comportex.topology.TwoDTopology{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$width,self__.width],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$height,self__.height],null))], null),self__.__extmap));
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$IIterable$ = true;

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__36517){
var self__ = this;
var G__36517__$1 = this;
return (new cljs.core.RecordIter((0),G__36517__$1,2,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$width,cljs.core.cst$kw$height], null),cljs.core._iterator(self__.__extmap)));
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.nfrac.comportex.topology.TwoDTopology(self__.width,self__.height,self__.__meta,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (2 + cljs.core.count(self__.__extmap));
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
var self__ = this;
var this__6762__auto____$1 = this;
var h__6588__auto__ = self__.__hash;
if(!((h__6588__auto__ == null))){
return h__6588__auto__;
} else {
var h__6588__auto____$1 = cljs.core.hash_imap(this__6762__auto____$1);
self__.__hash = h__6588__auto____$1;

return h__6588__auto____$1;
}
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
var self__ = this;
var this__6763__auto____$1 = this;
if(cljs.core.truth_((function (){var and__6141__auto__ = other__6764__auto__;
if(cljs.core.truth_(and__6141__auto__)){
var and__6141__auto____$1 = (this__6763__auto____$1.constructor === other__6764__auto__.constructor);
if(and__6141__auto____$1){
return cljs.core.equiv_map(this__6763__auto____$1,other__6764__auto__);
} else {
return and__6141__auto____$1;
}
} else {
return and__6141__auto__;
}
})())){
return true;
} else {
return false;
}
});

org.nfrac.comportex.topology.TwoDTopology.prototype.org$nfrac$comportex$protocols$PTopology$ = true;

org.nfrac.comportex.topology.TwoDTopology.prototype.org$nfrac$comportex$protocols$PTopology$dimensions$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [self__.width,self__.height], null);
});

org.nfrac.comportex.topology.TwoDTopology.prototype.org$nfrac$comportex$protocols$PTopology$coordinates_of_index$arity$2 = (function (_,idx){
var self__ = this;
var ___$1 = this;
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.rem(idx,self__.width),cljs.core.quot(idx,self__.width)], null);
});

org.nfrac.comportex.topology.TwoDTopology.prototype.org$nfrac$comportex$protocols$PTopology$index_of_coordinates$arity$2 = (function (_,coord){
var self__ = this;
var ___$1 = this;
var vec__36521 = coord;
var cx = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36521,(0),null);
var cy = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36521,(1),null);
return (cx + (cy * self__.width));
});

org.nfrac.comportex.topology.TwoDTopology.prototype.org$nfrac$comportex$protocols$PTopology$neighbours_STAR_$arity$4 = (function (this$,coord,outer_r,inner_r){
var self__ = this;
var this$__$1 = this;
var vec__36522 = coord;
var cx = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36522,(0),null);
var cy = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36522,(1),null);
var iter__6925__auto__ = ((function (vec__36522,cx,cy,this$__$1){
return (function org$nfrac$comportex$topology$iter__36523(s__36524){
return (new cljs.core.LazySeq(null,((function (vec__36522,cx,cy,this$__$1){
return (function (){
var s__36524__$1 = s__36524;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__36524__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var x = cljs.core.first(xs__5205__auto__);
var iterys__6921__auto__ = ((function (s__36524__$1,x,xs__5205__auto__,temp__4657__auto__,vec__36522,cx,cy,this$__$1){
return (function org$nfrac$comportex$topology$iter__36523_$_iter__36525(s__36526){
return (new cljs.core.LazySeq(null,((function (s__36524__$1,x,xs__5205__auto__,temp__4657__auto__,vec__36522,cx,cy,this$__$1){
return (function (){
var s__36526__$1 = s__36526;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__36526__$1);
if(temp__4657__auto____$1){
var s__36526__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__36526__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__36526__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__36528 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__36527 = (0);
while(true){
if((i__36527 < size__6924__auto__)){
var y = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__36527);
if(((org.nfrac.comportex.topology.abs((x - cx)) > inner_r)) || ((org.nfrac.comportex.topology.abs((y - cy)) > inner_r))){
cljs.core.chunk_append(b__36528,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x,y], null));

var G__36540 = (i__36527 + (1));
i__36527 = G__36540;
continue;
} else {
var G__36541 = (i__36527 + (1));
i__36527 = G__36541;
continue;
}
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__36528),org$nfrac$comportex$topology$iter__36523_$_iter__36525(cljs.core.chunk_rest(s__36526__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__36528),null);
}
} else {
var y = cljs.core.first(s__36526__$2);
if(((org.nfrac.comportex.topology.abs((x - cx)) > inner_r)) || ((org.nfrac.comportex.topology.abs((y - cy)) > inner_r))){
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x,y], null),org$nfrac$comportex$topology$iter__36523_$_iter__36525(cljs.core.rest(s__36526__$2)));
} else {
var G__36542 = cljs.core.rest(s__36526__$2);
s__36526__$1 = G__36542;
continue;
}
}
} else {
return null;
}
break;
}
});})(s__36524__$1,x,xs__5205__auto__,temp__4657__auto__,vec__36522,cx,cy,this$__$1))
,null,null));
});})(s__36524__$1,x,xs__5205__auto__,temp__4657__auto__,vec__36522,cx,cy,this$__$1))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$2((function (){var x__6484__auto__ = (cy - outer_r);
var y__6485__auto__ = (0);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})(),(function (){var x__6491__auto__ = ((cy + outer_r) + (1));
var y__6492__auto__ = self__.height;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})())));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,org$nfrac$comportex$topology$iter__36523(cljs.core.rest(s__36524__$1)));
} else {
var G__36543 = cljs.core.rest(s__36524__$1);
s__36524__$1 = G__36543;
continue;
}
} else {
return null;
}
break;
}
});})(vec__36522,cx,cy,this$__$1))
,null,null));
});})(vec__36522,cx,cy,this$__$1))
;
return iter__6925__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$2((function (){var x__6484__auto__ = (cx - outer_r);
var y__6485__auto__ = (0);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})(),(function (){var x__6491__auto__ = ((cx + outer_r) + (1));
var y__6492__auto__ = self__.width;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})()));
});

org.nfrac.comportex.topology.TwoDTopology.prototype.org$nfrac$comportex$protocols$PTopology$coord_distance$arity$3 = (function (_,coord_a,coord_b){
var self__ = this;
var ___$1 = this;
var vec__36534 = coord_a;
var xa = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36534,(0),null);
var ya = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36534,(1),null);
var vec__36535 = coord_b;
var xb = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36535,(0),null);
var yb = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36535,(1),null);
var x__6484__auto__ = org.nfrac.comportex.topology.abs((xb - xa));
var y__6485__auto__ = org.nfrac.comportex.topology.abs((yb - ya));
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$width,null,cljs.core.cst$kw$height,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.nfrac.comportex.topology.TwoDTopology(self__.width,self__.height,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__36517){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__36536 = cljs.core.keyword_identical_QMARK_;
var expr__36537 = k__6775__auto__;
if(cljs.core.truth_((pred__36536.cljs$core$IFn$_invoke$arity$2 ? pred__36536.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$width,expr__36537) : pred__36536.call(null,cljs.core.cst$kw$width,expr__36537)))){
return (new org.nfrac.comportex.topology.TwoDTopology(G__36517,self__.height,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36536.cljs$core$IFn$_invoke$arity$2 ? pred__36536.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$height,expr__36537) : pred__36536.call(null,cljs.core.cst$kw$height,expr__36537)))){
return (new org.nfrac.comportex.topology.TwoDTopology(self__.width,G__36517,self__.__meta,self__.__extmap,null));
} else {
return (new org.nfrac.comportex.topology.TwoDTopology(self__.width,self__.height,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__36517),null));
}
}
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$width,self__.width],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$height,self__.height],null))], null),self__.__extmap));
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__36517){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.nfrac.comportex.topology.TwoDTopology(self__.width,self__.height,G__36517,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.topology.TwoDTopology.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.nfrac.comportex.topology.TwoDTopology.getBasis = (function (){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$width,cljs.core.cst$sym$height], null);
});

org.nfrac.comportex.topology.TwoDTopology.cljs$lang$type = true;

org.nfrac.comportex.topology.TwoDTopology.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.nfrac.comportex.topology/TwoDTopology");
});

org.nfrac.comportex.topology.TwoDTopology.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.nfrac.comportex.topology/TwoDTopology");
});

org.nfrac.comportex.topology.__GT_TwoDTopology = (function org$nfrac$comportex$topology$__GT_TwoDTopology(width,height){
return (new org.nfrac.comportex.topology.TwoDTopology(width,height,null,null,null));
});

org.nfrac.comportex.topology.map__GT_TwoDTopology = (function org$nfrac$comportex$topology$map__GT_TwoDTopology(G__36519){
return (new org.nfrac.comportex.topology.TwoDTopology(cljs.core.cst$kw$width.cljs$core$IFn$_invoke$arity$1(G__36519),cljs.core.cst$kw$height.cljs$core$IFn$_invoke$arity$1(G__36519),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__36519,cljs.core.cst$kw$width,cljs.core.array_seq([cljs.core.cst$kw$height], 0)),null));
});

org.nfrac.comportex.topology.two_d_topology = (function org$nfrac$comportex$topology$two_d_topology(width,height){
return org.nfrac.comportex.topology.__GT_TwoDTopology(width,height);
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {org.nfrac.comportex.protocols.PTopology}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.nfrac.comportex.topology.ThreeDTopology = (function (width,height,depth,__meta,__extmap,__hash){
this.width = width;
this.height = height;
this.depth = depth;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k36545,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__36547 = (((k36545 instanceof cljs.core.Keyword))?k36545.fqn:null);
switch (G__36547) {
case "width":
return self__.width;

break;
case "height":
return self__.height;

break;
case "depth":
return self__.depth;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k36545,else__6770__auto__);

}
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.nfrac.comportex.topology.ThreeDTopology{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$width,self__.width],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$height,self__.height],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$depth,self__.depth],null))], null),self__.__extmap));
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$IIterable$ = true;

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__36544){
var self__ = this;
var G__36544__$1 = this;
return (new cljs.core.RecordIter((0),G__36544__$1,3,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$width,cljs.core.cst$kw$height,cljs.core.cst$kw$depth], null),cljs.core._iterator(self__.__extmap)));
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.nfrac.comportex.topology.ThreeDTopology(self__.width,self__.height,self__.depth,self__.__meta,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (3 + cljs.core.count(self__.__extmap));
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
var self__ = this;
var this__6762__auto____$1 = this;
var h__6588__auto__ = self__.__hash;
if(!((h__6588__auto__ == null))){
return h__6588__auto__;
} else {
var h__6588__auto____$1 = cljs.core.hash_imap(this__6762__auto____$1);
self__.__hash = h__6588__auto____$1;

return h__6588__auto____$1;
}
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
var self__ = this;
var this__6763__auto____$1 = this;
if(cljs.core.truth_((function (){var and__6141__auto__ = other__6764__auto__;
if(cljs.core.truth_(and__6141__auto__)){
var and__6141__auto____$1 = (this__6763__auto____$1.constructor === other__6764__auto__.constructor);
if(and__6141__auto____$1){
return cljs.core.equiv_map(this__6763__auto____$1,other__6764__auto__);
} else {
return and__6141__auto____$1;
}
} else {
return and__6141__auto__;
}
})())){
return true;
} else {
return false;
}
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.org$nfrac$comportex$protocols$PTopology$ = true;

org.nfrac.comportex.topology.ThreeDTopology.prototype.org$nfrac$comportex$protocols$PTopology$dimensions$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [self__.width,self__.height,self__.depth], null);
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.org$nfrac$comportex$protocols$PTopology$coordinates_of_index$arity$2 = (function (_,idx){
var self__ = this;
var ___$1 = this;
var z = cljs.core.quot(idx,(self__.width * self__.height));
var z_rem = cljs.core.rem(idx,(self__.width * self__.height));
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.rem(z_rem,self__.width),cljs.core.quot(z_rem,self__.width),z], null);
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.org$nfrac$comportex$protocols$PTopology$index_of_coordinates$arity$2 = (function (_,coord){
var self__ = this;
var ___$1 = this;
var vec__36548 = coord;
var cx = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36548,(0),null);
var cy = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36548,(1),null);
var cz = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36548,(2),null);
return ((cx + (cy * self__.width)) + ((cz * self__.width) * self__.height));
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.org$nfrac$comportex$protocols$PTopology$neighbours_STAR_$arity$4 = (function (this$,coord,outer_r,inner_r){
var self__ = this;
var this$__$1 = this;
var vec__36549 = coord;
var cx = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36549,(0),null);
var cy = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36549,(1),null);
var cz = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36549,(2),null);
var iter__6925__auto__ = ((function (vec__36549,cx,cy,cz,this$__$1){
return (function org$nfrac$comportex$topology$iter__36550(s__36551){
return (new cljs.core.LazySeq(null,((function (vec__36549,cx,cy,cz,this$__$1){
return (function (){
var s__36551__$1 = s__36551;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__36551__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var x = cljs.core.first(xs__5205__auto__);
var iterys__6921__auto__ = ((function (s__36551__$1,x,xs__5205__auto__,temp__4657__auto__,vec__36549,cx,cy,cz,this$__$1){
return (function org$nfrac$comportex$topology$iter__36550_$_iter__36552(s__36553){
return (new cljs.core.LazySeq(null,((function (s__36551__$1,x,xs__5205__auto__,temp__4657__auto__,vec__36549,cx,cy,cz,this$__$1){
return (function (){
var s__36553__$1 = s__36553;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__36553__$1);
if(temp__4657__auto____$1){
var xs__5205__auto____$1 = temp__4657__auto____$1;
var y = cljs.core.first(xs__5205__auto____$1);
var iterys__6921__auto__ = ((function (s__36553__$1,s__36551__$1,y,xs__5205__auto____$1,temp__4657__auto____$1,x,xs__5205__auto__,temp__4657__auto__,vec__36549,cx,cy,cz,this$__$1){
return (function org$nfrac$comportex$topology$iter__36550_$_iter__36552_$_iter__36554(s__36555){
return (new cljs.core.LazySeq(null,((function (s__36553__$1,s__36551__$1,y,xs__5205__auto____$1,temp__4657__auto____$1,x,xs__5205__auto__,temp__4657__auto__,vec__36549,cx,cy,cz,this$__$1){
return (function (){
var s__36555__$1 = s__36555;
while(true){
var temp__4657__auto____$2 = cljs.core.seq(s__36555__$1);
if(temp__4657__auto____$2){
var s__36555__$2 = temp__4657__auto____$2;
if(cljs.core.chunked_seq_QMARK_(s__36555__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__36555__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__36557 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__36556 = (0);
while(true){
if((i__36556 < size__6924__auto__)){
var z = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__36556);
if(((org.nfrac.comportex.topology.abs((x - cx)) > inner_r)) || ((org.nfrac.comportex.topology.abs((y - cy)) > inner_r)) || ((org.nfrac.comportex.topology.abs((z - cz)) > inner_r))){
cljs.core.chunk_append(b__36557,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [x,y,z], null));

var G__36575 = (i__36556 + (1));
i__36556 = G__36575;
continue;
} else {
var G__36576 = (i__36556 + (1));
i__36556 = G__36576;
continue;
}
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__36557),org$nfrac$comportex$topology$iter__36550_$_iter__36552_$_iter__36554(cljs.core.chunk_rest(s__36555__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__36557),null);
}
} else {
var z = cljs.core.first(s__36555__$2);
if(((org.nfrac.comportex.topology.abs((x - cx)) > inner_r)) || ((org.nfrac.comportex.topology.abs((y - cy)) > inner_r)) || ((org.nfrac.comportex.topology.abs((z - cz)) > inner_r))){
return cljs.core.cons(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [x,y,z], null),org$nfrac$comportex$topology$iter__36550_$_iter__36552_$_iter__36554(cljs.core.rest(s__36555__$2)));
} else {
var G__36577 = cljs.core.rest(s__36555__$2);
s__36555__$1 = G__36577;
continue;
}
}
} else {
return null;
}
break;
}
});})(s__36553__$1,s__36551__$1,y,xs__5205__auto____$1,temp__4657__auto____$1,x,xs__5205__auto__,temp__4657__auto__,vec__36549,cx,cy,cz,this$__$1))
,null,null));
});})(s__36553__$1,s__36551__$1,y,xs__5205__auto____$1,temp__4657__auto____$1,x,xs__5205__auto__,temp__4657__auto__,vec__36549,cx,cy,cz,this$__$1))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$2((function (){var x__6484__auto__ = (cz - outer_r);
var y__6485__auto__ = (0);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})(),(function (){var x__6491__auto__ = ((cz + outer_r) + (1));
var y__6492__auto__ = self__.depth;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})())));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,org$nfrac$comportex$topology$iter__36550_$_iter__36552(cljs.core.rest(s__36553__$1)));
} else {
var G__36578 = cljs.core.rest(s__36553__$1);
s__36553__$1 = G__36578;
continue;
}
} else {
return null;
}
break;
}
});})(s__36551__$1,x,xs__5205__auto__,temp__4657__auto__,vec__36549,cx,cy,cz,this$__$1))
,null,null));
});})(s__36551__$1,x,xs__5205__auto__,temp__4657__auto__,vec__36549,cx,cy,cz,this$__$1))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$2((function (){var x__6484__auto__ = (cy - outer_r);
var y__6485__auto__ = (0);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})(),(function (){var x__6491__auto__ = ((cy + outer_r) + (1));
var y__6492__auto__ = self__.height;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})())));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,org$nfrac$comportex$topology$iter__36550(cljs.core.rest(s__36551__$1)));
} else {
var G__36579 = cljs.core.rest(s__36551__$1);
s__36551__$1 = G__36579;
continue;
}
} else {
return null;
}
break;
}
});})(vec__36549,cx,cy,cz,this$__$1))
,null,null));
});})(vec__36549,cx,cy,cz,this$__$1))
;
return iter__6925__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$2((function (){var x__6484__auto__ = (cx - outer_r);
var y__6485__auto__ = (0);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})(),(function (){var x__6491__auto__ = ((cx + outer_r) + (1));
var y__6492__auto__ = self__.width;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})()));
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.org$nfrac$comportex$protocols$PTopology$coord_distance$arity$3 = (function (_,coord_a,coord_b){
var self__ = this;
var ___$1 = this;
var vec__36569 = coord_a;
var xa = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36569,(0),null);
var ya = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36569,(1),null);
var za = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36569,(2),null);
var vec__36570 = coord_b;
var xb = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36570,(0),null);
var yb = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36570,(1),null);
var zb = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36570,(2),null);
var x__6484__auto__ = (function (){var x__6484__auto__ = org.nfrac.comportex.topology.abs((xb - xa));
var y__6485__auto__ = org.nfrac.comportex.topology.abs((yb - ya));
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})();
var y__6485__auto__ = org.nfrac.comportex.topology.abs((zb - za));
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$width,null,cljs.core.cst$kw$depth,null,cljs.core.cst$kw$height,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.nfrac.comportex.topology.ThreeDTopology(self__.width,self__.height,self__.depth,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__36544){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__36571 = cljs.core.keyword_identical_QMARK_;
var expr__36572 = k__6775__auto__;
if(cljs.core.truth_((pred__36571.cljs$core$IFn$_invoke$arity$2 ? pred__36571.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$width,expr__36572) : pred__36571.call(null,cljs.core.cst$kw$width,expr__36572)))){
return (new org.nfrac.comportex.topology.ThreeDTopology(G__36544,self__.height,self__.depth,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36571.cljs$core$IFn$_invoke$arity$2 ? pred__36571.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$height,expr__36572) : pred__36571.call(null,cljs.core.cst$kw$height,expr__36572)))){
return (new org.nfrac.comportex.topology.ThreeDTopology(self__.width,G__36544,self__.depth,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36571.cljs$core$IFn$_invoke$arity$2 ? pred__36571.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$depth,expr__36572) : pred__36571.call(null,cljs.core.cst$kw$depth,expr__36572)))){
return (new org.nfrac.comportex.topology.ThreeDTopology(self__.width,self__.height,G__36544,self__.__meta,self__.__extmap,null));
} else {
return (new org.nfrac.comportex.topology.ThreeDTopology(self__.width,self__.height,self__.depth,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__36544),null));
}
}
}
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$width,self__.width],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$height,self__.height],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$depth,self__.depth],null))], null),self__.__extmap));
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__36544){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.nfrac.comportex.topology.ThreeDTopology(self__.width,self__.height,self__.depth,G__36544,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.topology.ThreeDTopology.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.nfrac.comportex.topology.ThreeDTopology.getBasis = (function (){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$width,cljs.core.cst$sym$height,cljs.core.cst$sym$depth], null);
});

org.nfrac.comportex.topology.ThreeDTopology.cljs$lang$type = true;

org.nfrac.comportex.topology.ThreeDTopology.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.nfrac.comportex.topology/ThreeDTopology");
});

org.nfrac.comportex.topology.ThreeDTopology.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.nfrac.comportex.topology/ThreeDTopology");
});

org.nfrac.comportex.topology.__GT_ThreeDTopology = (function org$nfrac$comportex$topology$__GT_ThreeDTopology(width,height,depth){
return (new org.nfrac.comportex.topology.ThreeDTopology(width,height,depth,null,null,null));
});

org.nfrac.comportex.topology.map__GT_ThreeDTopology = (function org$nfrac$comportex$topology$map__GT_ThreeDTopology(G__36546){
return (new org.nfrac.comportex.topology.ThreeDTopology(cljs.core.cst$kw$width.cljs$core$IFn$_invoke$arity$1(G__36546),cljs.core.cst$kw$height.cljs$core$IFn$_invoke$arity$1(G__36546),cljs.core.cst$kw$depth.cljs$core$IFn$_invoke$arity$1(G__36546),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__36546,cljs.core.cst$kw$width,cljs.core.array_seq([cljs.core.cst$kw$height,cljs.core.cst$kw$depth], 0)),null));
});

org.nfrac.comportex.topology.three_d_topology = (function org$nfrac$comportex$topology$three_d_topology(w,h,d){
return org.nfrac.comportex.topology.__GT_ThreeDTopology(w,h,d);
});
org.nfrac.comportex.topology.make_topology = (function org$nfrac$comportex$topology$make_topology(dims){
var vec__36582 = dims;
var w = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36582,(0),null);
var h = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36582,(1),null);
var d = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36582,(2),null);
var q = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36582,(3),null);
var G__36583 = cljs.core.count(dims);
switch (G__36583) {
case (0):
return org.nfrac.comportex.topology.one_d_topology((0));

break;
case (1):
return org.nfrac.comportex.topology.one_d_topology(w);

break;
case (2):
return org.nfrac.comportex.topology.two_d_topology(w,h);

break;
case (3):
return org.nfrac.comportex.topology.three_d_topology(w,h,d);

break;
case (4):
return org.nfrac.comportex.topology.three_d_topology(w,h,(d * q));

break;
default:
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(cljs.core.count(dims))].join('')));

}
});
org.nfrac.comportex.topology.empty_topology = org.nfrac.comportex.topology.make_topology(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0)], null));
/**
 * Project n dimensions to n-1 dimensions by eliminating the last dimension.
 * 
 *   This removes potentially-valuable structure.
 *   Example: in dimensions [8 7 6], the points [0 0 0] [0 1 0] are adjacent.
 *   After squashing to [8 42], these points [0 0] [0 6] are much further apart.
 */
org.nfrac.comportex.topology.squash_last_dimension = (function org$nfrac$comportex$topology$squash_last_dimension(dims){
return cljs.core.vec(cljs.core.butlast(cljs.core.update_in.cljs$core$IFn$_invoke$arity$4(dims,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(cljs.core.count(dims) - (2))], null),cljs.core._STAR_,cljs.core.last(dims))));
});
/**
 * Project n dimensions to n+1 dimensions by dividing the first dimension
 *   into cross sections.
 * 
 *   This artificially adds structure. It can also disrupt existing structure.
 *   Example: In dimensions [64] the points [7] and [8] are adjacent.
 *   After splitting to [8 8], these points [0 7] [1 0] are further apart.
 */
org.nfrac.comportex.topology.split_first_dimension = (function org$nfrac$comportex$topology$split_first_dimension(dims,xsection_length){
var temp__4657__auto__ = dims;
if(cljs.core.truth_(temp__4657__auto__)){
var vec__36586 = temp__4657__auto__;
var x = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36586,(0),null);
var rest = cljs.core.nthnext(vec__36586,(1));
if((cljs.core.rem(x,xsection_length) === (0))){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.quot(x,xsection_length)], null),cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(dims,(0),xsection_length));
} else {
return null;
}
} else {
return null;
}
});
/**
 * Align n topologies along the x axis into a single topology.
 *   If the topologies don't stack neatly, force compatibility via two
 *   strategies:
 * 
 *   1. Add dimensions to the lower-dimensional topology by splitting its first
 *   dimension into cross sections. This is analogous to summing numbers encoded
 *   in a mixed radix. If the sum of `higher` and `lower` can be expressed by only
 *   changing the first digit of `higher`, then the two can be stacked in
 *   `higher`'s radix (i.e. dimensions).
 * 
 *   Default behavior: don't redistribute / mangle `lower`'s lower dimensions
 *   (i.e. [y, z, ...]). To force mangling, provide a 1-dimensional `lower`.
 * 
 *   2. Remove dimensions from the higher-dimension topology by squashing its
 *   last two dimensions into one.
 * 
 *   It's best to hand-pick compatible topologies if topology matters.
 */
org.nfrac.comportex.topology.combined_dimensions = (function org$nfrac$comportex$topology$combined_dimensions(var_args){
var args36588 = [];
var len__7211__auto___36594 = arguments.length;
var i__7212__auto___36595 = (0);
while(true){
if((i__7212__auto___36595 < len__7211__auto___36594)){
args36588.push((arguments[i__7212__auto___36595]));

var G__36596 = (i__7212__auto___36595 + (1));
i__7212__auto___36595 = G__36596;
continue;
} else {
}
break;
}

var G__36591 = args36588.length;
switch (G__36591) {
case 0:
return org.nfrac.comportex.topology.combined_dimensions.cljs$core$IFn$_invoke$arity$0();

break;
default:
var argseq__7230__auto__ = (new cljs.core.IndexedSeq(args36588.slice((0)),(0)));
return org.nfrac.comportex.topology.combined_dimensions.cljs$core$IFn$_invoke$arity$variadic(argseq__7230__auto__);

}
});

org.nfrac.comportex.topology.combined_dimensions.cljs$core$IFn$_invoke$arity$0 = (function (){
return new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0)], null);
});

org.nfrac.comportex.topology.combined_dimensions.cljs$core$IFn$_invoke$arity$variadic = (function (all_dims){
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$2((function (dims1,dims2){
while(true){
var vec__36592 = cljs.core.sort_by.cljs$core$IFn$_invoke$arity$2(cljs.core.count,cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (dims1,dims2){
return (function (p1__36587_SHARP_){
if(cljs.core.empty_QMARK_(p1__36587_SHARP_)){
return new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0)], null);
} else {
return p1__36587_SHARP_;
}
});})(dims1,dims2))
,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [dims1,dims2], null)));
var lower = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36592,(0),null);
var higher = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36592,(1),null);
var disparity = (cljs.core.count(higher) - cljs.core.count(lower));
var vec__36593 = cljs.core.split_at(disparity,cljs.core.rest(higher));
var to_match = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36593,(0),null);
var must_already_match = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36593,(1),null);
var temp__4655__auto__ = ((cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.vec(cljs.core.rest(lower)),cljs.core.vec(must_already_match)))?cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(org.nfrac.comportex.topology.split_first_dimension,lower,cljs.core.reverse(to_match)):null);
if(cljs.core.truth_(temp__4655__auto__)){
var compatible = temp__4655__auto__;
return cljs.core.update_in.cljs$core$IFn$_invoke$arity$4(higher,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0)], null),cljs.core._PLUS_,cljs.core.first(compatible));
} else {
var G__36598 = org.nfrac.comportex.topology.squash_last_dimension(higher);
var G__36599 = lower;
dims1 = G__36598;
dims2 = G__36599;
continue;
}
break;
}
}),all_dims);
});

org.nfrac.comportex.topology.combined_dimensions.cljs$lang$applyTo = (function (seq36589){
return org.nfrac.comportex.topology.combined_dimensions.cljs$core$IFn$_invoke$arity$variadic(cljs.core.seq(seq36589));
});

org.nfrac.comportex.topology.combined_dimensions.cljs$lang$maxFixedArity = (0);
