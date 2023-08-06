// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.bridge.marshalling');
goog.require('cljs.core');
goog.require('cljs.core.async');
goog.require('cljs.core.async.impl.protocols');
goog.require('cognitect.transit');

/**
 * @interface
 */
org.numenta.sanity.bridge.marshalling.PMarshalled = function(){};

org.numenta.sanity.bridge.marshalling.release_BANG_ = (function org$numenta$sanity$bridge$marshalling$release_BANG_(this$){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$bridge$marshalling$PMarshalled$release_BANG_$arity$1 == null)))){
return this$.org$numenta$sanity$bridge$marshalling$PMarshalled$release_BANG_$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.bridge.marshalling.release_BANG_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.bridge.marshalling.release_BANG_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PMarshalled.release!",this$);
}
}
}
});


/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.numenta.sanity.bridge.marshalling.PMarshalled}
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
org.numenta.sanity.bridge.marshalling.ChannelMarshal = (function (ch,single_use_QMARK_,released_QMARK_,__meta,__extmap,__hash){
this.ch = ch;
this.single_use_QMARK_ = single_use_QMARK_;
this.released_QMARK_ = released_QMARK_;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k46049,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__46051 = (((k46049 instanceof cljs.core.Keyword))?k46049.fqn:null);
switch (G__46051) {
case "ch":
return self__.ch;

break;
case "single-use?":
return self__.single_use_QMARK_;

break;
case "released?":
return self__.released_QMARK_;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k46049,else__6770__auto__);

}
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.org$numenta$sanity$bridge$marshalling$PMarshalled$ = true;

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.org$numenta$sanity$bridge$marshalling$PMarshalled$release_BANG_$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(self__.released_QMARK_,true) : cljs.core.reset_BANG_.call(null,self__.released_QMARK_,true));
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.numenta.sanity.bridge.marshalling.ChannelMarshal{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$ch,self__.ch],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$single_DASH_use_QMARK_,self__.single_use_QMARK_],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$released_QMARK_,self__.released_QMARK_],null))], null),self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$IIterable$ = true;

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__46048){
var self__ = this;
var G__46048__$1 = this;
return (new cljs.core.RecordIter((0),G__46048__$1,3,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$ch,cljs.core.cst$kw$single_DASH_use_QMARK_,cljs.core.cst$kw$released_QMARK_], null),cljs.core._iterator(self__.__extmap)));
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.numenta.sanity.bridge.marshalling.ChannelMarshal(self__.ch,self__.single_use_QMARK_,self__.released_QMARK_,self__.__meta,self__.__extmap,self__.__hash));
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (3 + cljs.core.count(self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$ch,null,cljs.core.cst$kw$single_DASH_use_QMARK_,null,cljs.core.cst$kw$released_QMARK_,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.numenta.sanity.bridge.marshalling.ChannelMarshal(self__.ch,self__.single_use_QMARK_,self__.released_QMARK_,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__46048){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__46052 = cljs.core.keyword_identical_QMARK_;
var expr__46053 = k__6775__auto__;
if(cljs.core.truth_((pred__46052.cljs$core$IFn$_invoke$arity$2 ? pred__46052.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$ch,expr__46053) : pred__46052.call(null,cljs.core.cst$kw$ch,expr__46053)))){
return (new org.numenta.sanity.bridge.marshalling.ChannelMarshal(G__46048,self__.single_use_QMARK_,self__.released_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__46052.cljs$core$IFn$_invoke$arity$2 ? pred__46052.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$single_DASH_use_QMARK_,expr__46053) : pred__46052.call(null,cljs.core.cst$kw$single_DASH_use_QMARK_,expr__46053)))){
return (new org.numenta.sanity.bridge.marshalling.ChannelMarshal(self__.ch,G__46048,self__.released_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__46052.cljs$core$IFn$_invoke$arity$2 ? pred__46052.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$released_QMARK_,expr__46053) : pred__46052.call(null,cljs.core.cst$kw$released_QMARK_,expr__46053)))){
return (new org.numenta.sanity.bridge.marshalling.ChannelMarshal(self__.ch,self__.single_use_QMARK_,G__46048,self__.__meta,self__.__extmap,null));
} else {
return (new org.numenta.sanity.bridge.marshalling.ChannelMarshal(self__.ch,self__.single_use_QMARK_,self__.released_QMARK_,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__46048),null));
}
}
}
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$ch,self__.ch],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$single_DASH_use_QMARK_,self__.single_use_QMARK_],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$released_QMARK_,self__.released_QMARK_],null))], null),self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__46048){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.numenta.sanity.bridge.marshalling.ChannelMarshal(self__.ch,self__.single_use_QMARK_,self__.released_QMARK_,G__46048,self__.__extmap,self__.__hash));
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.getBasis = (function (){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$ch,cljs.core.cst$sym$single_DASH_use_QMARK_,cljs.core.cst$sym$released_QMARK_], null);
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.cljs$lang$type = true;

org.numenta.sanity.bridge.marshalling.ChannelMarshal.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.numenta.sanity.bridge.marshalling/ChannelMarshal");
});

org.numenta.sanity.bridge.marshalling.ChannelMarshal.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.numenta.sanity.bridge.marshalling/ChannelMarshal");
});

org.numenta.sanity.bridge.marshalling.__GT_ChannelMarshal = (function org$numenta$sanity$bridge$marshalling$__GT_ChannelMarshal(ch,single_use_QMARK_,released_QMARK_){
return (new org.numenta.sanity.bridge.marshalling.ChannelMarshal(ch,single_use_QMARK_,released_QMARK_,null,null,null));
});

org.numenta.sanity.bridge.marshalling.map__GT_ChannelMarshal = (function org$numenta$sanity$bridge$marshalling$map__GT_ChannelMarshal(G__46050){
return (new org.numenta.sanity.bridge.marshalling.ChannelMarshal(cljs.core.cst$kw$ch.cljs$core$IFn$_invoke$arity$1(G__46050),cljs.core.cst$kw$single_DASH_use_QMARK_.cljs$core$IFn$_invoke$arity$1(G__46050),cljs.core.cst$kw$released_QMARK_.cljs$core$IFn$_invoke$arity$1(G__46050),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__46050,cljs.core.cst$kw$ch,cljs.core.array_seq([cljs.core.cst$kw$single_DASH_use_QMARK_,cljs.core.cst$kw$released_QMARK_], 0)),null));
});

/**
 * Allows a channel to be marshalled across the network.
 * 
 *   When Client A serializes a ChannelMarshal, Client A will assign it a target-id
 *   and send the target-id across the network. When decoding the message, Client B
 *   will set the decoded ChannelMarshal's :ch field to a ChannelProxy. Any `put!`
 *   or `close!` on a ChannelProxy will be delivered across the network back to
 *   Client A.
 * 
 *   Client B should not send a ChannelMarshal back to Client A. It will create a
 *   silly chain of proxies. Use `channel-weak`.
 * 
 *   All of this assumes that the network code on both clients is using
 *   write-handlers and read-handlers that follow this protocol.
 */
org.numenta.sanity.bridge.marshalling.channel = (function org$numenta$sanity$bridge$marshalling$channel(var_args){
var args46056 = [];
var len__7211__auto___46059 = arguments.length;
var i__7212__auto___46060 = (0);
while(true){
if((i__7212__auto___46060 < len__7211__auto___46059)){
args46056.push((arguments[i__7212__auto___46060]));

var G__46061 = (i__7212__auto___46060 + (1));
i__7212__auto___46060 = G__46061;
continue;
} else {
}
break;
}

var G__46058 = args46056.length;
switch (G__46058) {
case 1:
return org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$1((arguments[(0)]));

break;
case 2:
return org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args46056.length)].join('')));

}
});

org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$1 = (function (ch){
return org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(ch,false);
});

org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2 = (function (ch,single_use_QMARK_){
return (new org.numenta.sanity.bridge.marshalling.ChannelMarshal(ch,single_use_QMARK_,(cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(false) : cljs.core.atom.call(null,false)),null,null,null));
});

org.numenta.sanity.bridge.marshalling.channel.cljs$lang$maxFixedArity = 2;

/**
* @constructor
 * @implements {cljs.core.IRecord}
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
org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal = (function (target_id,__meta,__extmap,__hash){
this.target_id = target_id;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k46064,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__46066 = (((k46064 instanceof cljs.core.Keyword))?k46064.fqn:null);
switch (G__46066) {
case "target-id":
return self__.target_id;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k46064,else__6770__auto__);

}
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$target_DASH_id,self__.target_id],null))], null),self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$IIterable$ = true;

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__46063){
var self__ = this;
var G__46063__$1 = this;
return (new cljs.core.RecordIter((0),G__46063__$1,1,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$target_DASH_id], null),cljs.core._iterator(self__.__extmap)));
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal(self__.target_id,self__.__meta,self__.__extmap,self__.__hash));
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (1 + cljs.core.count(self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$target_DASH_id,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal(self__.target_id,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__46063){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__46067 = cljs.core.keyword_identical_QMARK_;
var expr__46068 = k__6775__auto__;
if(cljs.core.truth_((pred__46067.cljs$core$IFn$_invoke$arity$2 ? pred__46067.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$target_DASH_id,expr__46068) : pred__46067.call(null,cljs.core.cst$kw$target_DASH_id,expr__46068)))){
return (new org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal(G__46063,self__.__meta,self__.__extmap,null));
} else {
return (new org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal(self__.target_id,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__46063),null));
}
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$target_DASH_id,self__.target_id],null))], null),self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__46063){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal(self__.target_id,G__46063,self__.__extmap,self__.__hash));
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.getBasis = (function (){
return new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$target_DASH_id], null);
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.cljs$lang$type = true;

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.numenta.sanity.bridge.marshalling/ChannelWeakMarshal");
});

org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.numenta.sanity.bridge.marshalling/ChannelWeakMarshal");
});

org.numenta.sanity.bridge.marshalling.__GT_ChannelWeakMarshal = (function org$numenta$sanity$bridge$marshalling$__GT_ChannelWeakMarshal(target_id){
return (new org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal(target_id,null,null,null));
});

org.numenta.sanity.bridge.marshalling.map__GT_ChannelWeakMarshal = (function org$numenta$sanity$bridge$marshalling$map__GT_ChannelWeakMarshal(G__46065){
return (new org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal(cljs.core.cst$kw$target_DASH_id.cljs$core$IFn$_invoke$arity$1(G__46065),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(G__46065,cljs.core.cst$kw$target_DASH_id),null));
});

/**
 * Allows a marshalled channel to be referred to without creating chains of
 *   proxies.
 * 
 *   When a client decodes a message containing a ChannelWeakMarshal, it will check
 *   if this target-id belongs to this client. If it does, this ChannelWeakMarshal
 *   will be 'decoded' into its original ChannelMarshal. This allows Client B to
 *   tell Client A 'If we get disconnected, send me this data blob on reconnect,
 *   and I'll remember you'. This allows the data blob to contain channels that are
 *   usable again on second send without causing a chain of proxies.
 * 
 *   All of this assumes that the network code on both clients is using
 *   write-handlers and read-handlers that follow this protocol.
 */
org.numenta.sanity.bridge.marshalling.channel_weak = (function org$numenta$sanity$bridge$marshalling$channel_weak(target_id){
return (new org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal(target_id,null,null,null));
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.numenta.sanity.bridge.marshalling.PMarshalled}
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
org.numenta.sanity.bridge.marshalling.BigValueMarshal = (function (resource_id,value,pushed_QMARK_,released_QMARK_,__meta,__extmap,__hash){
this.resource_id = resource_id;
this.value = value;
this.pushed_QMARK_ = pushed_QMARK_;
this.released_QMARK_ = released_QMARK_;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k46072,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__46074 = (((k46072 instanceof cljs.core.Keyword))?k46072.fqn:null);
switch (G__46074) {
case "resource-id":
return self__.resource_id;

break;
case "value":
return self__.value;

break;
case "pushed?":
return self__.pushed_QMARK_;

break;
case "released?":
return self__.released_QMARK_;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k46072,else__6770__auto__);

}
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.org$numenta$sanity$bridge$marshalling$PMarshalled$ = true;

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.org$numenta$sanity$bridge$marshalling$PMarshalled$release_BANG_$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(self__.released_QMARK_,true) : cljs.core.reset_BANG_.call(null,self__.released_QMARK_,true));
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.numenta.sanity.bridge.marshalling.BigValueMarshal{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$resource_DASH_id,self__.resource_id],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$value,self__.value],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$pushed_QMARK_,self__.pushed_QMARK_],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$released_QMARK_,self__.released_QMARK_],null))], null),self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$IIterable$ = true;

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__46071){
var self__ = this;
var G__46071__$1 = this;
return (new cljs.core.RecordIter((0),G__46071__$1,4,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$resource_DASH_id,cljs.core.cst$kw$value,cljs.core.cst$kw$pushed_QMARK_,cljs.core.cst$kw$released_QMARK_], null),cljs.core._iterator(self__.__extmap)));
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.numenta.sanity.bridge.marshalling.BigValueMarshal(self__.resource_id,self__.value,self__.pushed_QMARK_,self__.released_QMARK_,self__.__meta,self__.__extmap,self__.__hash));
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (4 + cljs.core.count(self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$value,null,cljs.core.cst$kw$resource_DASH_id,null,cljs.core.cst$kw$pushed_QMARK_,null,cljs.core.cst$kw$released_QMARK_,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.numenta.sanity.bridge.marshalling.BigValueMarshal(self__.resource_id,self__.value,self__.pushed_QMARK_,self__.released_QMARK_,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__46071){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__46075 = cljs.core.keyword_identical_QMARK_;
var expr__46076 = k__6775__auto__;
if(cljs.core.truth_((pred__46075.cljs$core$IFn$_invoke$arity$2 ? pred__46075.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$resource_DASH_id,expr__46076) : pred__46075.call(null,cljs.core.cst$kw$resource_DASH_id,expr__46076)))){
return (new org.numenta.sanity.bridge.marshalling.BigValueMarshal(G__46071,self__.value,self__.pushed_QMARK_,self__.released_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__46075.cljs$core$IFn$_invoke$arity$2 ? pred__46075.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$value,expr__46076) : pred__46075.call(null,cljs.core.cst$kw$value,expr__46076)))){
return (new org.numenta.sanity.bridge.marshalling.BigValueMarshal(self__.resource_id,G__46071,self__.pushed_QMARK_,self__.released_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__46075.cljs$core$IFn$_invoke$arity$2 ? pred__46075.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$pushed_QMARK_,expr__46076) : pred__46075.call(null,cljs.core.cst$kw$pushed_QMARK_,expr__46076)))){
return (new org.numenta.sanity.bridge.marshalling.BigValueMarshal(self__.resource_id,self__.value,G__46071,self__.released_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__46075.cljs$core$IFn$_invoke$arity$2 ? pred__46075.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$released_QMARK_,expr__46076) : pred__46075.call(null,cljs.core.cst$kw$released_QMARK_,expr__46076)))){
return (new org.numenta.sanity.bridge.marshalling.BigValueMarshal(self__.resource_id,self__.value,self__.pushed_QMARK_,G__46071,self__.__meta,self__.__extmap,null));
} else {
return (new org.numenta.sanity.bridge.marshalling.BigValueMarshal(self__.resource_id,self__.value,self__.pushed_QMARK_,self__.released_QMARK_,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__46071),null));
}
}
}
}
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$resource_DASH_id,self__.resource_id],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$value,self__.value],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$pushed_QMARK_,self__.pushed_QMARK_],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$released_QMARK_,self__.released_QMARK_],null))], null),self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__46071){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.numenta.sanity.bridge.marshalling.BigValueMarshal(self__.resource_id,self__.value,self__.pushed_QMARK_,self__.released_QMARK_,G__46071,self__.__extmap,self__.__hash));
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.getBasis = (function (){
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$resource_DASH_id,cljs.core.cst$sym$value,cljs.core.cst$sym$pushed_QMARK_,cljs.core.cst$sym$released_QMARK_], null);
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.cljs$lang$type = true;

org.numenta.sanity.bridge.marshalling.BigValueMarshal.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.numenta.sanity.bridge.marshalling/BigValueMarshal");
});

org.numenta.sanity.bridge.marshalling.BigValueMarshal.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.numenta.sanity.bridge.marshalling/BigValueMarshal");
});

org.numenta.sanity.bridge.marshalling.__GT_BigValueMarshal = (function org$numenta$sanity$bridge$marshalling$__GT_BigValueMarshal(resource_id,value,pushed_QMARK_,released_QMARK_){
return (new org.numenta.sanity.bridge.marshalling.BigValueMarshal(resource_id,value,pushed_QMARK_,released_QMARK_,null,null,null));
});

org.numenta.sanity.bridge.marshalling.map__GT_BigValueMarshal = (function org$numenta$sanity$bridge$marshalling$map__GT_BigValueMarshal(G__46073){
return (new org.numenta.sanity.bridge.marshalling.BigValueMarshal(cljs.core.cst$kw$resource_DASH_id.cljs$core$IFn$_invoke$arity$1(G__46073),cljs.core.cst$kw$value.cljs$core$IFn$_invoke$arity$1(G__46073),cljs.core.cst$kw$pushed_QMARK_.cljs$core$IFn$_invoke$arity$1(G__46073),cljs.core.cst$kw$released_QMARK_.cljs$core$IFn$_invoke$arity$1(G__46073),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__46073,cljs.core.cst$kw$resource_DASH_id,cljs.core.array_seq([cljs.core.cst$kw$value,cljs.core.cst$kw$pushed_QMARK_,cljs.core.cst$kw$released_QMARK_], 0)),null));
});

/**
 * Put a value in a box labelled 'recipients should cache this so that I don't
 *   have to send it every time.'
 * 
 *   When Client B decodes a message containing a BigValueMarshal, it will save the
 *   value and tell Client A that it has saved the value. Later, when Client A
 *   serializes the same BigValueMarshal to send it to Client B, it will only
 *   include the resource-id, and Client B will reinsert the value when it decodes
 *   the message.
 * 
 *   Call `release!` on a BigValueMarshal to tell other machines that they can
 *   release it.
 * 
 *   All of this assumes that the network code on both clients is using
 *   write-handlers and read-handlers that follow this protocol.
 */
org.numenta.sanity.bridge.marshalling.big_value = (function org$numenta$sanity$bridge$marshalling$big_value(value){
return (new org.numenta.sanity.bridge.marshalling.BigValueMarshal(cljs.core.random_uuid(),value,false,(cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(false) : cljs.core.atom.call(null,false)),null,null,null));
});
org.numenta.sanity.bridge.marshalling.future = (function org$numenta$sanity$bridge$marshalling$future(val){
if(typeof org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082 !== 'undefined'){
} else {

/**
* @constructor
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.IDeref}
 * @implements {cljs.core.IWithMeta}
*/
org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082 = (function (future,val,meta46083){
this.future = future;
this.val = val;
this.meta46083 = meta46083;
this.cljs$lang$protocol_mask$partition0$ = 425984;
this.cljs$lang$protocol_mask$partition1$ = 0;
})
org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (_46084,meta46083__$1){
var self__ = this;
var _46084__$1 = this;
return (new org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082(self__.future,self__.val,meta46083__$1));
});

org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082.prototype.cljs$core$IMeta$_meta$arity$1 = (function (_46084){
var self__ = this;
var _46084__$1 = this;
return self__.meta46083;
});

org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082.prototype.cljs$core$IDeref$_deref$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return self__.val;
});

org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082.getBasis = (function (){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.with_meta(cljs.core.cst$sym$future,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$arglists,cljs.core.list(cljs.core.cst$sym$quote,cljs.core.list(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$val], null)))], null)),cljs.core.cst$sym$val,cljs.core.cst$sym$meta46083], null);
});

org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082.cljs$lang$type = true;

org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082.cljs$lang$ctorStr = "org.numenta.sanity.bridge.marshalling/t_org$numenta$sanity$bridge$marshalling46082";

org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082.cljs$lang$ctorPrWriter = (function (this__6751__auto__,writer__6752__auto__,opt__6753__auto__){
return cljs.core._write(writer__6752__auto__,"org.numenta.sanity.bridge.marshalling/t_org$numenta$sanity$bridge$marshalling46082");
});

org.numenta.sanity.bridge.marshalling.__GT_t_org$numenta$sanity$bridge$marshalling46082 = (function org$numenta$sanity$bridge$marshalling$future_$___GT_t_org$numenta$sanity$bridge$marshalling46082(future__$1,val__$1,meta46083){
return (new org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082(future__$1,val__$1,meta46083));
});

}

return (new org.numenta.sanity.bridge.marshalling.t_org$numenta$sanity$bridge$marshalling46082(org$numenta$sanity$bridge$marshalling$future,val,cljs.core.PersistentArrayMap.EMPTY));
});

/**
* @constructor
 * @implements {cljs.core.async.impl.protocols.Channel}
 * @implements {cljs.core.async.impl.protocols.WritePort}
 * @implements {cljs.core.async.impl.protocols.ReadPort}
*/
org.numenta.sanity.bridge.marshalling.ImpersonateChannel = (function (fput,fclose,ftake){
this.fput = fput;
this.fclose = fclose;
this.ftake = ftake;
})
org.numenta.sanity.bridge.marshalling.ImpersonateChannel.prototype.cljs$core$async$impl$protocols$ReadPort$ = true;

org.numenta.sanity.bridge.marshalling.ImpersonateChannel.prototype.cljs$core$async$impl$protocols$ReadPort$take_BANG_$arity$2 = (function (_,___$1){
var self__ = this;
var ___$2 = this;
return org.numenta.sanity.bridge.marshalling.future((self__.ftake.cljs$core$IFn$_invoke$arity$0 ? self__.ftake.cljs$core$IFn$_invoke$arity$0() : self__.ftake.call(null)));
});

org.numenta.sanity.bridge.marshalling.ImpersonateChannel.prototype.cljs$core$async$impl$protocols$WritePort$ = true;

org.numenta.sanity.bridge.marshalling.ImpersonateChannel.prototype.cljs$core$async$impl$protocols$WritePort$put_BANG_$arity$3 = (function (_,v,___$1){
var self__ = this;
var ___$2 = this;
if(cljs.core.truth_(v)){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.cst$sym$v], 0)))].join('')));
}

return org.numenta.sanity.bridge.marshalling.future((self__.fput.cljs$core$IFn$_invoke$arity$1 ? self__.fput.cljs$core$IFn$_invoke$arity$1(v) : self__.fput.call(null,v)));
});

org.numenta.sanity.bridge.marshalling.ImpersonateChannel.prototype.cljs$core$async$impl$protocols$Channel$ = true;

org.numenta.sanity.bridge.marshalling.ImpersonateChannel.prototype.cljs$core$async$impl$protocols$Channel$close_BANG_$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return (self__.fclose.cljs$core$IFn$_invoke$arity$0 ? self__.fclose.cljs$core$IFn$_invoke$arity$0() : self__.fclose.call(null));
});

org.numenta.sanity.bridge.marshalling.ImpersonateChannel.getBasis = (function (){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$fput,cljs.core.cst$sym$fclose,cljs.core.cst$sym$ftake], null);
});

org.numenta.sanity.bridge.marshalling.ImpersonateChannel.cljs$lang$type = true;

org.numenta.sanity.bridge.marshalling.ImpersonateChannel.cljs$lang$ctorStr = "org.numenta.sanity.bridge.marshalling/ImpersonateChannel";

org.numenta.sanity.bridge.marshalling.ImpersonateChannel.cljs$lang$ctorPrWriter = (function (this__6751__auto__,writer__6752__auto__,opt__6753__auto__){
return cljs.core._write(writer__6752__auto__,"org.numenta.sanity.bridge.marshalling/ImpersonateChannel");
});

org.numenta.sanity.bridge.marshalling.__GT_ImpersonateChannel = (function org$numenta$sanity$bridge$marshalling$__GT_ImpersonateChannel(fput,fclose,ftake){
return (new org.numenta.sanity.bridge.marshalling.ImpersonateChannel(fput,fclose,ftake));
});


/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {cljs.core.async.impl.protocols.Channel}
 * @implements {cljs.core.async.impl.protocols.WritePort}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.async.impl.protocols.ReadPort}
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
org.numenta.sanity.bridge.marshalling.ChannelProxy = (function (target_id,ch,__meta,__extmap,__hash){
this.target_id = target_id;
this.ch = ch;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$async$impl$protocols$ReadPort$ = true;

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$async$impl$protocols$ReadPort$take_BANG_$arity$2 = (function (_,handler){
var self__ = this;
var ___$1 = this;
return cljs.core.async.impl.protocols.take_BANG_(self__.ch,handler);
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$async$impl$protocols$Channel$ = true;

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$async$impl$protocols$Channel$close_BANG_$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return cljs.core.async.impl.protocols.close_BANG_(self__.ch);
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k46086,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__46088 = (((k46086 instanceof cljs.core.Keyword))?k46086.fqn:null);
switch (G__46088) {
case "target-id":
return self__.target_id;

break;
case "ch":
return self__.ch;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k46086,else__6770__auto__);

}
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.numenta.sanity.bridge.marshalling.ChannelProxy{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$target_DASH_id,self__.target_id],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$ch,self__.ch],null))], null),self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$IIterable$ = true;

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__46085){
var self__ = this;
var G__46085__$1 = this;
return (new cljs.core.RecordIter((0),G__46085__$1,2,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$target_DASH_id,cljs.core.cst$kw$ch], null),cljs.core._iterator(self__.__extmap)));
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.numenta.sanity.bridge.marshalling.ChannelProxy(self__.target_id,self__.ch,self__.__meta,self__.__extmap,self__.__hash));
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (2 + cljs.core.count(self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$async$impl$protocols$WritePort$ = true;

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$async$impl$protocols$WritePort$put_BANG_$arity$3 = (function (_,v,handler){
var self__ = this;
var ___$1 = this;
return cljs.core.async.impl.protocols.put_BANG_(self__.ch,v,handler);
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$target_DASH_id,null,cljs.core.cst$kw$ch,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.numenta.sanity.bridge.marshalling.ChannelProxy(self__.target_id,self__.ch,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__46085){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__46089 = cljs.core.keyword_identical_QMARK_;
var expr__46090 = k__6775__auto__;
if(cljs.core.truth_((pred__46089.cljs$core$IFn$_invoke$arity$2 ? pred__46089.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$target_DASH_id,expr__46090) : pred__46089.call(null,cljs.core.cst$kw$target_DASH_id,expr__46090)))){
return (new org.numenta.sanity.bridge.marshalling.ChannelProxy(G__46085,self__.ch,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__46089.cljs$core$IFn$_invoke$arity$2 ? pred__46089.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$ch,expr__46090) : pred__46089.call(null,cljs.core.cst$kw$ch,expr__46090)))){
return (new org.numenta.sanity.bridge.marshalling.ChannelProxy(self__.target_id,G__46085,self__.__meta,self__.__extmap,null));
} else {
return (new org.numenta.sanity.bridge.marshalling.ChannelProxy(self__.target_id,self__.ch,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__46085),null));
}
}
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$target_DASH_id,self__.target_id],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$ch,self__.ch],null))], null),self__.__extmap));
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__46085){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.numenta.sanity.bridge.marshalling.ChannelProxy(self__.target_id,self__.ch,G__46085,self__.__extmap,self__.__hash));
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.getBasis = (function (){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$target_DASH_id,cljs.core.cst$sym$ch], null);
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.cljs$lang$type = true;

org.numenta.sanity.bridge.marshalling.ChannelProxy.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.numenta.sanity.bridge.marshalling/ChannelProxy");
});

org.numenta.sanity.bridge.marshalling.ChannelProxy.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.numenta.sanity.bridge.marshalling/ChannelProxy");
});

org.numenta.sanity.bridge.marshalling.__GT_ChannelProxy = (function org$numenta$sanity$bridge$marshalling$__GT_ChannelProxy(target_id,ch){
return (new org.numenta.sanity.bridge.marshalling.ChannelProxy(target_id,ch,null,null,null));
});

org.numenta.sanity.bridge.marshalling.map__GT_ChannelProxy = (function org$numenta$sanity$bridge$marshalling$map__GT_ChannelProxy(G__46087){
return (new org.numenta.sanity.bridge.marshalling.ChannelProxy(cljs.core.cst$kw$target_DASH_id.cljs$core$IFn$_invoke$arity$1(G__46087),cljs.core.cst$kw$ch.cljs$core$IFn$_invoke$arity$1(G__46087),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__46087,cljs.core.cst$kw$target_DASH_id,cljs.core.array_seq([cljs.core.cst$kw$ch], 0)),null));
});

org.numenta.sanity.bridge.marshalling.encoding = cljs.core.cst$kw$json;
org.numenta.sanity.bridge.marshalling.write_handlers = (function org$numenta$sanity$bridge$marshalling$write_handlers(target__GT_mchannel,local_resources){
return cljs.core.PersistentArrayMap.fromArray([org.numenta.sanity.bridge.marshalling.ChannelMarshal,cognitect.transit.write_handler.cljs$core$IFn$_invoke$arity$2((function (_){
return "ChannelMarshal";
}),(function (mchannel){
var target_id = cljs.core.random_uuid();
var released_QMARK_ = cljs.core.cst$kw$released_QMARK_.cljs$core$IFn$_invoke$arity$1(mchannel);
if(cljs.core.not((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(released_QMARK_) : cljs.core.deref.call(null,released_QMARK_)))){
cljs.core.add_watch(released_QMARK_,cljs.core.random_uuid(),((function (target_id,released_QMARK_){
return (function (_,___$1,___$2,r_QMARK_){
if(cljs.core.truth_(r_QMARK_)){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(target__GT_mchannel,cljs.core.dissoc,target_id);
} else {
return null;
}
});})(target_id,released_QMARK_))
);

cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(target__GT_mchannel,cljs.core.assoc,target_id,mchannel);

return target_id;
} else {
return cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["Serializing a released channel!",mchannel], 0));
}
})),org.numenta.sanity.bridge.marshalling.ChannelWeakMarshal,cognitect.transit.write_handler.cljs$core$IFn$_invoke$arity$2((function (_){
return "ChannelWeakMarshal";
}),(function (wmchannel){
return cljs.core.cst$kw$target_DASH_id.cljs$core$IFn$_invoke$arity$1(wmchannel);
})),org.numenta.sanity.bridge.marshalling.BigValueMarshal,cognitect.transit.write_handler.cljs$core$IFn$_invoke$arity$2((function (_){
return "BigValueMarshal";
}),(function (marshal){
var map__46122 = marshal;
var map__46122__$1 = ((((!((map__46122 == null)))?((((map__46122.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46122.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46122):map__46122);
var released_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46122__$1,cljs.core.cst$kw$released_QMARK_);
var resource_id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46122__$1,cljs.core.cst$kw$resource_DASH_id);
if(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(released_QMARK_) : cljs.core.deref.call(null,released_QMARK_)))){
} else {
if(cljs.core.contains_QMARK_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(local_resources) : cljs.core.deref.call(null,local_resources)),resource_id)){
} else {
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(local_resources,cljs.core.assoc,resource_id,marshal);

cljs.core.add_watch(released_QMARK_,local_resources,((function (map__46122,map__46122__$1,released_QMARK_,resource_id){
return (function (_,___$1,___$2,r_QMARK_){
if(cljs.core.truth_(r_QMARK_)){
cljs.core.remove_watch(released_QMARK_,local_resources);

var temp__4657__auto___46151 = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(local_resources) : cljs.core.deref.call(null,local_resources)),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [resource_id,cljs.core.cst$kw$on_DASH_released_DASH_c], null));
if(cljs.core.truth_(temp__4657__auto___46151)){
var ch_46152 = temp__4657__auto___46151;
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(ch_46152,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$release], null));
} else {
}

return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(local_resources,cljs.core.dissoc,resource_id);
} else {
return null;
}
});})(map__46122,map__46122__$1,released_QMARK_,resource_id))
);
}
}

if(cljs.core.truth_(cljs.core.get_in.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(local_resources) : cljs.core.deref.call(null,local_resources)),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [resource_id,cljs.core.cst$kw$pushed_QMARK_], null)))){
return new cljs.core.PersistentArrayMap(null, 1, ["resource-id",resource_id], null);
} else {
var saved_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var c__38109__auto___46153 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___46153,saved_c,map__46122,map__46122__$1,released_QMARK_,resource_id){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___46153,saved_c,map__46122,map__46122__$1,released_QMARK_,resource_id){
return (function (state_46136){
var state_val_46137 = (state_46136[(1)]);
if((state_val_46137 === (1))){
var state_46136__$1 = state_46136;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_46136__$1,(2),saved_c);
} else {
if((state_val_46137 === (2))){
var inst_46125 = (state_46136[(7)]);
var inst_46125__$1 = (state_46136[(2)]);
var state_46136__$1 = (function (){var statearr_46138 = state_46136;
(statearr_46138[(7)] = inst_46125__$1);

return statearr_46138;
})();
if(cljs.core.truth_(inst_46125__$1)){
var statearr_46139_46154 = state_46136__$1;
(statearr_46139_46154[(1)] = (3));

} else {
var statearr_46140_46155 = state_46136__$1;
(statearr_46140_46155[(1)] = (4));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_46137 === (3))){
var inst_46125 = (state_46136[(7)]);
var inst_46128 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_46125,(0),null);
var inst_46129 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_46125,(1),null);
var inst_46130 = (function (){var temp__4657__auto__ = inst_46125;
var vec__46127 = inst_46125;
var _ = inst_46128;
var on_released_c_marshal = inst_46129;
return ((function (temp__4657__auto__,vec__46127,_,on_released_c_marshal,inst_46125,inst_46128,inst_46129,state_val_46137,c__38109__auto___46153,saved_c,map__46122,map__46122__$1,released_QMARK_,resource_id){
return (function (marshal__$1){
var G__46141 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(marshal__$1,cljs.core.cst$kw$pushed_QMARK_,true);
if(cljs.core.truth_(on_released_c_marshal)){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__46141,cljs.core.cst$kw$on_DASH_released_DASH_c,cljs.core.cst$kw$ch.cljs$core$IFn$_invoke$arity$1(on_released_c_marshal));
} else {
return G__46141;
}
});
;})(temp__4657__auto__,vec__46127,_,on_released_c_marshal,inst_46125,inst_46128,inst_46129,state_val_46137,c__38109__auto___46153,saved_c,map__46122,map__46122__$1,released_QMARK_,resource_id))
})();
var inst_46131 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(local_resources,cljs.core.update,resource_id,inst_46130);
var state_46136__$1 = state_46136;
var statearr_46142_46156 = state_46136__$1;
(statearr_46142_46156[(2)] = inst_46131);

(statearr_46142_46156[(1)] = (5));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46137 === (4))){
var state_46136__$1 = state_46136;
var statearr_46143_46157 = state_46136__$1;
(statearr_46143_46157[(2)] = null);

(statearr_46143_46157[(1)] = (5));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46137 === (5))){
var inst_46134 = (state_46136[(2)]);
var state_46136__$1 = state_46136;
return cljs.core.async.impl.ioc_helpers.return_chan(state_46136__$1,inst_46134);
} else {
return null;
}
}
}
}
}
});})(c__38109__auto___46153,saved_c,map__46122,map__46122__$1,released_QMARK_,resource_id))
;
return ((function (switch__37995__auto__,c__38109__auto___46153,saved_c,map__46122,map__46122__$1,released_QMARK_,resource_id){
return (function() {
var org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto____0 = (function (){
var statearr_46147 = [null,null,null,null,null,null,null,null];
(statearr_46147[(0)] = org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto__);

(statearr_46147[(1)] = (1));

return statearr_46147;
});
var org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto____1 = (function (state_46136){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_46136);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e46148){if((e46148 instanceof Object)){
var ex__37999__auto__ = e46148;
var statearr_46149_46158 = state_46136;
(statearr_46149_46158[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_46136);

return cljs.core.cst$kw$recur;
} else {
throw e46148;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__46159 = state_46136;
state_46136 = G__46159;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto__ = function(state_46136){
switch(arguments.length){
case 0:
return org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto____1.call(this,state_46136);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto____0;
org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto____1;
return org$numenta$sanity$bridge$marshalling$write_handlers_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___46153,saved_c,map__46122,map__46122__$1,released_QMARK_,resource_id))
})();
var state__38111__auto__ = (function (){var statearr_46150 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_46150[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___46153);

return statearr_46150;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___46153,saved_c,map__46122,map__46122__$1,released_QMARK_,resource_id))
);


return new cljs.core.PersistentArrayMap(null, 3, ["resource-id",resource_id,"value",cljs.core.cst$kw$value.cljs$core$IFn$_invoke$arity$1(marshal),"on-saved-c-marshal",org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(saved_c,true)], null);
}
}))], true, false);
});
org.numenta.sanity.bridge.marshalling.read_handlers = (function org$numenta$sanity$bridge$marshalling$read_handlers(target__GT_mchannel,fput,fclose,remote_resources){
return new cljs.core.PersistentArrayMap(null, 3, ["ChannelMarshal",cognitect.transit.read_handler((function (target_id){
return org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$1((new org.numenta.sanity.bridge.marshalling.ChannelProxy(target_id,(new org.numenta.sanity.bridge.marshalling.ImpersonateChannel((function (v){
return (fput.cljs$core$IFn$_invoke$arity$2 ? fput.cljs$core$IFn$_invoke$arity$2(target_id,v) : fput.call(null,target_id,v));
}),(function (){
return (fclose.cljs$core$IFn$_invoke$arity$1 ? fclose.cljs$core$IFn$_invoke$arity$1(target_id) : fclose.call(null,target_id));
}),null)),null,null,null)));
})),"ChannelWeakMarshal",cognitect.transit.read_handler((function (target_id){
var temp__4655__auto__ = cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(target__GT_mchannel) : cljs.core.deref.call(null,target__GT_mchannel)),target_id);
if(cljs.core.truth_(temp__4655__auto__)){
var mchannel = temp__4655__auto__;
return mchannel;
} else {
return org.numenta.sanity.bridge.marshalling.channel_weak(target_id);
}
})),"BigValueMarshal",cognitect.transit.read_handler((function (m){
var map__46184 = m;
var map__46184__$1 = ((((!((map__46184 == null)))?((((map__46184.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46184.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46184):map__46184);
var resource_id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46184__$1,"resource-id");
var on_saved_c_marshal = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46184__$1,"on-saved-c-marshal");
var new_QMARK_ = !(cljs.core.contains_QMARK_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(remote_resources) : cljs.core.deref.call(null,remote_resources)),resource_id));
if(new_QMARK_){
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(remote_resources,cljs.core.assoc,resource_id,(new org.numenta.sanity.bridge.marshalling.BigValueMarshal(resource_id,cljs.core.get.cljs$core$IFn$_invoke$arity$2(m,"value"),null,null,null,null,null)));
} else {
}

if(cljs.core.truth_(on_saved_c_marshal)){
var on_released_c_marshal_46208 = ((new_QMARK_)?(function (){var ch = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var c__38109__auto___46209 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___46209,ch,map__46184,map__46184__$1,resource_id,on_saved_c_marshal,new_QMARK_){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___46209,ch,map__46184,map__46184__$1,resource_id,on_saved_c_marshal,new_QMARK_){
return (function (state_46195){
var state_val_46196 = (state_46195[(1)]);
if((state_val_46196 === (1))){
var state_46195__$1 = state_46195;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_46195__$1,(2),ch);
} else {
if((state_val_46196 === (2))){
var inst_46187 = (state_46195[(2)]);
var inst_46188 = (inst_46187 == null);
var state_46195__$1 = state_46195;
if(cljs.core.truth_(inst_46188)){
var statearr_46197_46210 = state_46195__$1;
(statearr_46197_46210[(1)] = (3));

} else {
var statearr_46198_46211 = state_46195__$1;
(statearr_46198_46211[(1)] = (4));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_46196 === (3))){
var state_46195__$1 = state_46195;
var statearr_46199_46212 = state_46195__$1;
(statearr_46199_46212[(2)] = null);

(statearr_46199_46212[(1)] = (5));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46196 === (4))){
var inst_46191 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(remote_resources,cljs.core.dissoc,resource_id);
var state_46195__$1 = state_46195;
var statearr_46200_46213 = state_46195__$1;
(statearr_46200_46213[(2)] = inst_46191);

(statearr_46200_46213[(1)] = (5));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46196 === (5))){
var inst_46193 = (state_46195[(2)]);
var state_46195__$1 = state_46195;
return cljs.core.async.impl.ioc_helpers.return_chan(state_46195__$1,inst_46193);
} else {
return null;
}
}
}
}
}
});})(c__38109__auto___46209,ch,map__46184,map__46184__$1,resource_id,on_saved_c_marshal,new_QMARK_))
;
return ((function (switch__37995__auto__,c__38109__auto___46209,ch,map__46184,map__46184__$1,resource_id,on_saved_c_marshal,new_QMARK_){
return (function() {
var org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto____0 = (function (){
var statearr_46204 = [null,null,null,null,null,null,null];
(statearr_46204[(0)] = org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto__);

(statearr_46204[(1)] = (1));

return statearr_46204;
});
var org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto____1 = (function (state_46195){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_46195);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e46205){if((e46205 instanceof Object)){
var ex__37999__auto__ = e46205;
var statearr_46206_46214 = state_46195;
(statearr_46206_46214[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_46195);

return cljs.core.cst$kw$recur;
} else {
throw e46205;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__46215 = state_46195;
state_46195 = G__46215;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto__ = function(state_46195){
switch(arguments.length){
case 0:
return org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto____1.call(this,state_46195);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto____0;
org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto____1;
return org$numenta$sanity$bridge$marshalling$read_handlers_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___46209,ch,map__46184,map__46184__$1,resource_id,on_saved_c_marshal,new_QMARK_))
})();
var state__38111__auto__ = (function (){var statearr_46207 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_46207[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___46209);

return statearr_46207;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___46209,ch,map__46184,map__46184__$1,resource_id,on_saved_c_marshal,new_QMARK_))
);


return org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$1(ch);
})():null);
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$ch.cljs$core$IFn$_invoke$arity$1(on_saved_c_marshal),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$saved,on_released_c_marshal_46208], null));
} else {
}

return cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(remote_resources) : cljs.core.deref.call(null,remote_resources)),resource_id);
}))], null);
});
