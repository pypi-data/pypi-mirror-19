// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('tailrecursion.priority_map');
goog.require('cljs.core');
goog.require('cljs.core');
goog.require('cljs.reader');

/**
* @constructor
 * @implements {cljs.core.IReversible}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.IFn}
 * @implements {cljs.core.ICollection}
 * @implements {cljs.core.IEmptyableCollection}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISorted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.IStack}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
tailrecursion.priority_map.PersistentPriorityMap = (function (priority__GT_set_of_items,item__GT_priority,meta,keyfn,__hash){
this.priority__GT_set_of_items = priority__GT_set_of_items;
this.item__GT_priority = item__GT_priority;
this.meta = meta;
this.keyfn = keyfn;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2565220111;
this.cljs$lang$protocol_mask$partition1$ = 0;
})
tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this$,item){
var self__ = this;
var this$__$1 = this;
return cljs.core.get.cljs$core$IFn$_invoke$arity$2(self__.item__GT_priority,item);
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (coll,item,not_found){
var self__ = this;
var coll__$1 = this;
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.item__GT_priority,item,not_found);
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (coll,writer,opts){
var self__ = this;
var coll__$1 = this;
var pr_pair = ((function (coll__$1){
return (function (keyval){
return cljs.core.pr_sequential_writer(writer,cljs.core.pr_writer,""," ","",opts,keyval);
});})(coll__$1))
;
return cljs.core.pr_sequential_writer(writer,pr_pair,"#tailrecursion.priority-map {",", ","}",opts,coll__$1);
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
return self__.meta;
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$ICounted$_count$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
return cljs.core.count(self__.item__GT_priority);
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IStack$_peek$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
if((cljs.core.count(self__.item__GT_priority) === (0))){
return null;
} else {
var f = cljs.core.first(self__.priority__GT_set_of_items);
var item = cljs.core.first(cljs.core.val(f));
if(cljs.core.truth_(self__.keyfn)){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,(self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1 ? self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1(item) : self__.item__GT_priority.call(null,item))], null);
} else {
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,cljs.core.key(f)], null);
}
}
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IStack$_pop$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
if((cljs.core.count(self__.item__GT_priority) === (0))){
throw (new Error("Can't pop empty priority map"));
} else {
var f = cljs.core.first(self__.priority__GT_set_of_items);
var item_set = cljs.core.val(f);
var item = cljs.core.first(item_set);
var priority_key = cljs.core.key(f);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.count(item_set),(1))){
return (new tailrecursion.priority_map.PersistentPriorityMap(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.priority__GT_set_of_items,priority_key),cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.item__GT_priority,item),self__.meta,self__.keyfn,null));
} else {
return (new tailrecursion.priority_map.PersistentPriorityMap(cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.priority__GT_set_of_items,priority_key,cljs.core.disj.cljs$core$IFn$_invoke$arity$2(item_set,item)),cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.item__GT_priority,item),self__.meta,self__.keyfn,null));
}
}
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IReversible$_rseq$arity$1 = (function (coll){
var self__ = this;
var coll__$1 = this;
if(cljs.core.truth_(self__.keyfn)){
return cljs.core.seq((function (){var iter__6925__auto__ = ((function (coll__$1){
return (function tailrecursion$priority_map$iter__46774(s__46775){
return (new cljs.core.LazySeq(null,((function (coll__$1){
return (function (){
var s__46775__$1 = s__46775;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__46775__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var vec__46784 = cljs.core.first(xs__5205__auto__);
var priority = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46784,(0),null);
var item_set = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46784,(1),null);
var iterys__6921__auto__ = ((function (s__46775__$1,vec__46784,priority,item_set,xs__5205__auto__,temp__4657__auto__,coll__$1){
return (function tailrecursion$priority_map$iter__46774_$_iter__46776(s__46777){
return (new cljs.core.LazySeq(null,((function (s__46775__$1,vec__46784,priority,item_set,xs__5205__auto__,temp__4657__auto__,coll__$1){
return (function (){
var s__46777__$1 = s__46777;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__46777__$1);
if(temp__4657__auto____$1){
var s__46777__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__46777__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__46777__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__46779 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__46778 = (0);
while(true){
if((i__46778 < size__6924__auto__)){
var item = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__46778);
cljs.core.chunk_append(b__46779,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,(self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1 ? self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1(item) : self__.item__GT_priority.call(null,item))], null));

var G__46853 = (i__46778 + (1));
i__46778 = G__46853;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__46779),tailrecursion$priority_map$iter__46774_$_iter__46776(cljs.core.chunk_rest(s__46777__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__46779),null);
}
} else {
var item = cljs.core.first(s__46777__$2);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,(self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1 ? self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1(item) : self__.item__GT_priority.call(null,item))], null),tailrecursion$priority_map$iter__46774_$_iter__46776(cljs.core.rest(s__46777__$2)));
}
} else {
return null;
}
break;
}
});})(s__46775__$1,vec__46784,priority,item_set,xs__5205__auto__,temp__4657__auto__,coll__$1))
,null,null));
});})(s__46775__$1,vec__46784,priority,item_set,xs__5205__auto__,temp__4657__auto__,coll__$1))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(item_set));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,tailrecursion$priority_map$iter__46774(cljs.core.rest(s__46775__$1)));
} else {
var G__46854 = cljs.core.rest(s__46775__$1);
s__46775__$1 = G__46854;
continue;
}
} else {
return null;
}
break;
}
});})(coll__$1))
,null,null));
});})(coll__$1))
;
return iter__6925__auto__(cljs.core.rseq(self__.priority__GT_set_of_items));
})());
} else {
return cljs.core.seq((function (){var iter__6925__auto__ = ((function (coll__$1){
return (function tailrecursion$priority_map$iter__46787(s__46788){
return (new cljs.core.LazySeq(null,((function (coll__$1){
return (function (){
var s__46788__$1 = s__46788;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__46788__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var vec__46797 = cljs.core.first(xs__5205__auto__);
var priority = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46797,(0),null);
var item_set = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46797,(1),null);
var iterys__6921__auto__ = ((function (s__46788__$1,vec__46797,priority,item_set,xs__5205__auto__,temp__4657__auto__,coll__$1){
return (function tailrecursion$priority_map$iter__46787_$_iter__46789(s__46790){
return (new cljs.core.LazySeq(null,((function (s__46788__$1,vec__46797,priority,item_set,xs__5205__auto__,temp__4657__auto__,coll__$1){
return (function (){
var s__46790__$1 = s__46790;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__46790__$1);
if(temp__4657__auto____$1){
var s__46790__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__46790__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__46790__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__46792 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__46791 = (0);
while(true){
if((i__46791 < size__6924__auto__)){
var item = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__46791);
cljs.core.chunk_append(b__46792,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,priority], null));

var G__46855 = (i__46791 + (1));
i__46791 = G__46855;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__46792),tailrecursion$priority_map$iter__46787_$_iter__46789(cljs.core.chunk_rest(s__46790__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__46792),null);
}
} else {
var item = cljs.core.first(s__46790__$2);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,priority], null),tailrecursion$priority_map$iter__46787_$_iter__46789(cljs.core.rest(s__46790__$2)));
}
} else {
return null;
}
break;
}
});})(s__46788__$1,vec__46797,priority,item_set,xs__5205__auto__,temp__4657__auto__,coll__$1))
,null,null));
});})(s__46788__$1,vec__46797,priority,item_set,xs__5205__auto__,temp__4657__auto__,coll__$1))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(item_set));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,tailrecursion$priority_map$iter__46787(cljs.core.rest(s__46788__$1)));
} else {
var G__46856 = cljs.core.rest(s__46788__$1);
s__46788__$1 = G__46856;
continue;
}
} else {
return null;
}
break;
}
});})(coll__$1))
,null,null));
});})(coll__$1))
;
return iter__6925__auto__(cljs.core.rseq(self__.priority__GT_set_of_items));
})());
}
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IHash$_hash$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
var h__6588__auto__ = self__.__hash;
if(!((h__6588__auto__ == null))){
return h__6588__auto__;
} else {
var h__6588__auto____$1 = cljs.core.hash_imap(this$__$1);
self__.__hash = h__6588__auto____$1;

return h__6588__auto____$1;
}
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this$,other){
var self__ = this;
var this$__$1 = this;
return cljs.core._equiv(self__.item__GT_priority,other);
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IEmptyableCollection$_empty$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
return cljs.core.with_meta(tailrecursion.priority_map.PersistentPriorityMap.EMPTY,self__.meta);
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this$,item){
var self__ = this;
var this$__$1 = this;
var priority = (self__.item__GT_priority.cljs$core$IFn$_invoke$arity$2 ? self__.item__GT_priority.cljs$core$IFn$_invoke$arity$2(item,cljs.core.cst$kw$tailrecursion$priority_DASH_map_SLASH_not_DASH_found) : self__.item__GT_priority.call(null,item,cljs.core.cst$kw$tailrecursion$priority_DASH_map_SLASH_not_DASH_found));
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(priority,cljs.core.cst$kw$tailrecursion$priority_DASH_map_SLASH_not_DASH_found)){
return this$__$1;
} else {
var priority_key = (self__.keyfn.cljs$core$IFn$_invoke$arity$1 ? self__.keyfn.cljs$core$IFn$_invoke$arity$1(priority) : self__.keyfn.call(null,priority));
var item_set = (self__.priority__GT_set_of_items.cljs$core$IFn$_invoke$arity$1 ? self__.priority__GT_set_of_items.cljs$core$IFn$_invoke$arity$1(priority_key) : self__.priority__GT_set_of_items.call(null,priority_key));
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.count(item_set),(1))){
return (new tailrecursion.priority_map.PersistentPriorityMap(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.priority__GT_set_of_items,priority_key),cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.item__GT_priority,item),self__.meta,self__.keyfn,null));
} else {
return (new tailrecursion.priority_map.PersistentPriorityMap(cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.priority__GT_set_of_items,priority_key,cljs.core.disj.cljs$core$IFn$_invoke$arity$2(item_set,item)),cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.item__GT_priority,item),self__.meta,self__.keyfn,null));
}
}
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this$,item,priority){
var self__ = this;
var this$__$1 = this;
var temp__4655__auto__ = cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.item__GT_priority,item,null);
if(cljs.core.truth_(temp__4655__auto__)){
var current_priority = temp__4655__auto__;
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(current_priority,priority)){
return this$__$1;
} else {
var priority_key = (self__.keyfn.cljs$core$IFn$_invoke$arity$1 ? self__.keyfn.cljs$core$IFn$_invoke$arity$1(priority) : self__.keyfn.call(null,priority));
var current_priority_key = (self__.keyfn.cljs$core$IFn$_invoke$arity$1 ? self__.keyfn.cljs$core$IFn$_invoke$arity$1(current_priority) : self__.keyfn.call(null,current_priority));
var item_set = cljs.core.get.cljs$core$IFn$_invoke$arity$2(self__.priority__GT_set_of_items,current_priority_key);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.count(item_set),(1))){
return (new tailrecursion.priority_map.PersistentPriorityMap(cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.priority__GT_set_of_items,current_priority_key),priority_key,cljs.core.conj.cljs$core$IFn$_invoke$arity$2(cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.priority__GT_set_of_items,priority_key,cljs.core.PersistentHashSet.EMPTY),item)),cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.item__GT_priority,item,priority),self__.meta,self__.keyfn,null));
} else {
return (new tailrecursion.priority_map.PersistentPriorityMap(cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(self__.priority__GT_set_of_items,current_priority,cljs.core.disj.cljs$core$IFn$_invoke$arity$2(cljs.core.get.cljs$core$IFn$_invoke$arity$2(self__.priority__GT_set_of_items,current_priority_key),item),cljs.core.array_seq([priority,cljs.core.conj.cljs$core$IFn$_invoke$arity$2(cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.priority__GT_set_of_items,priority_key,cljs.core.PersistentHashSet.EMPTY),item)], 0)),cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.item__GT_priority,item,priority),self__.meta,self__.keyfn,null));
}
}
} else {
var priority_key = (self__.keyfn.cljs$core$IFn$_invoke$arity$1 ? self__.keyfn.cljs$core$IFn$_invoke$arity$1(priority) : self__.keyfn.call(null,priority));
return (new tailrecursion.priority_map.PersistentPriorityMap(cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.priority__GT_set_of_items,priority_key,cljs.core.conj.cljs$core$IFn$_invoke$arity$2(cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.priority__GT_set_of_items,priority_key,cljs.core.PersistentHashSet.EMPTY),item)),cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.item__GT_priority,item,priority),self__.meta,self__.keyfn,null));
}
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IAssociative$_contains_key_QMARK_$arity$2 = (function (this$,item){
var self__ = this;
var this$__$1 = this;
return cljs.core.contains_QMARK_(self__.item__GT_priority,item);
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
if(cljs.core.truth_(self__.keyfn)){
return cljs.core.seq((function (){var iter__6925__auto__ = ((function (this$__$1){
return (function tailrecursion$priority_map$iter__46800(s__46801){
return (new cljs.core.LazySeq(null,((function (this$__$1){
return (function (){
var s__46801__$1 = s__46801;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__46801__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var vec__46810 = cljs.core.first(xs__5205__auto__);
var priority = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46810,(0),null);
var item_set = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46810,(1),null);
var iterys__6921__auto__ = ((function (s__46801__$1,vec__46810,priority,item_set,xs__5205__auto__,temp__4657__auto__,this$__$1){
return (function tailrecursion$priority_map$iter__46800_$_iter__46802(s__46803){
return (new cljs.core.LazySeq(null,((function (s__46801__$1,vec__46810,priority,item_set,xs__5205__auto__,temp__4657__auto__,this$__$1){
return (function (){
var s__46803__$1 = s__46803;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__46803__$1);
if(temp__4657__auto____$1){
var s__46803__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__46803__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__46803__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__46805 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__46804 = (0);
while(true){
if((i__46804 < size__6924__auto__)){
var item = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__46804);
cljs.core.chunk_append(b__46805,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,(self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1 ? self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1(item) : self__.item__GT_priority.call(null,item))], null));

var G__46857 = (i__46804 + (1));
i__46804 = G__46857;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__46805),tailrecursion$priority_map$iter__46800_$_iter__46802(cljs.core.chunk_rest(s__46803__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__46805),null);
}
} else {
var item = cljs.core.first(s__46803__$2);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,(self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1 ? self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1(item) : self__.item__GT_priority.call(null,item))], null),tailrecursion$priority_map$iter__46800_$_iter__46802(cljs.core.rest(s__46803__$2)));
}
} else {
return null;
}
break;
}
});})(s__46801__$1,vec__46810,priority,item_set,xs__5205__auto__,temp__4657__auto__,this$__$1))
,null,null));
});})(s__46801__$1,vec__46810,priority,item_set,xs__5205__auto__,temp__4657__auto__,this$__$1))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(item_set));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,tailrecursion$priority_map$iter__46800(cljs.core.rest(s__46801__$1)));
} else {
var G__46858 = cljs.core.rest(s__46801__$1);
s__46801__$1 = G__46858;
continue;
}
} else {
return null;
}
break;
}
});})(this$__$1))
,null,null));
});})(this$__$1))
;
return iter__6925__auto__(self__.priority__GT_set_of_items);
})());
} else {
return cljs.core.seq((function (){var iter__6925__auto__ = ((function (this$__$1){
return (function tailrecursion$priority_map$iter__46813(s__46814){
return (new cljs.core.LazySeq(null,((function (this$__$1){
return (function (){
var s__46814__$1 = s__46814;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__46814__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var vec__46823 = cljs.core.first(xs__5205__auto__);
var priority = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46823,(0),null);
var item_set = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46823,(1),null);
var iterys__6921__auto__ = ((function (s__46814__$1,vec__46823,priority,item_set,xs__5205__auto__,temp__4657__auto__,this$__$1){
return (function tailrecursion$priority_map$iter__46813_$_iter__46815(s__46816){
return (new cljs.core.LazySeq(null,((function (s__46814__$1,vec__46823,priority,item_set,xs__5205__auto__,temp__4657__auto__,this$__$1){
return (function (){
var s__46816__$1 = s__46816;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__46816__$1);
if(temp__4657__auto____$1){
var s__46816__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__46816__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__46816__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__46818 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__46817 = (0);
while(true){
if((i__46817 < size__6924__auto__)){
var item = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__46817);
cljs.core.chunk_append(b__46818,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,priority], null));

var G__46859 = (i__46817 + (1));
i__46817 = G__46859;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__46818),tailrecursion$priority_map$iter__46813_$_iter__46815(cljs.core.chunk_rest(s__46816__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__46818),null);
}
} else {
var item = cljs.core.first(s__46816__$2);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,priority], null),tailrecursion$priority_map$iter__46813_$_iter__46815(cljs.core.rest(s__46816__$2)));
}
} else {
return null;
}
break;
}
});})(s__46814__$1,vec__46823,priority,item_set,xs__5205__auto__,temp__4657__auto__,this$__$1))
,null,null));
});})(s__46814__$1,vec__46823,priority,item_set,xs__5205__auto__,temp__4657__auto__,this$__$1))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(item_set));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,tailrecursion$priority_map$iter__46813(cljs.core.rest(s__46814__$1)));
} else {
var G__46860 = cljs.core.rest(s__46814__$1);
s__46814__$1 = G__46860;
continue;
}
} else {
return null;
}
break;
}
});})(this$__$1))
,null,null));
});})(this$__$1))
;
return iter__6925__auto__(self__.priority__GT_set_of_items);
})());
}
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this$,meta__$1){
var self__ = this;
var this$__$1 = this;
return (new tailrecursion.priority_map.PersistentPriorityMap(self__.priority__GT_set_of_items,self__.item__GT_priority,meta__$1,self__.keyfn,self__.__hash));
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this$,entry){
var self__ = this;
var this$__$1 = this;
if(cljs.core.vector_QMARK_(entry)){
return cljs.core._assoc(this$__$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this$__$1,entry);
}
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.call = (function() {
var G__46861 = null;
var G__46861__2 = (function (self__,item){
var self__ = this;
var self____$1 = this;
var this$ = self____$1;
return this$.cljs$core$ILookup$_lookup$arity$2(null,item);
});
var G__46861__3 = (function (self__,item,not_found){
var self__ = this;
var self____$1 = this;
var this$ = self____$1;
return this$.cljs$core$ILookup$_lookup$arity$3(null,item,not_found);
});
G__46861 = function(self__,item,not_found){
switch(arguments.length){
case 2:
return G__46861__2.call(this,self__,item);
case 3:
return G__46861__3.call(this,self__,item,not_found);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
G__46861.cljs$core$IFn$_invoke$arity$2 = G__46861__2;
G__46861.cljs$core$IFn$_invoke$arity$3 = G__46861__3;
return G__46861;
})()
;

tailrecursion.priority_map.PersistentPriorityMap.prototype.apply = (function (self__,args46773){
var self__ = this;
var self____$1 = this;
return self____$1.call.apply(self____$1,[self____$1].concat(cljs.core.aclone(args46773)));
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IFn$_invoke$arity$1 = (function (item){
var self__ = this;
var this$ = this;
return this$.cljs$core$ILookup$_lookup$arity$2(null,item);
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$IFn$_invoke$arity$2 = (function (item,not_found){
var self__ = this;
var this$ = this;
return this$.cljs$core$ILookup$_lookup$arity$3(null,item,not_found);
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$ISorted$_sorted_seq$arity$2 = (function (this$,ascending_QMARK_){
var self__ = this;
var this$__$1 = this;
return (cljs.core.truth_(ascending_QMARK_)?cljs.core.seq:cljs.core.rseq).call(null,this$__$1);
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$ISorted$_sorted_seq_from$arity$3 = (function (this$,k,ascending_QMARK_){
var self__ = this;
var this$__$1 = this;
var sets = (cljs.core.truth_(ascending_QMARK_)?cljs.core.subseq.cljs$core$IFn$_invoke$arity$3(self__.priority__GT_set_of_items,cljs.core._GT__EQ_,k):cljs.core.rsubseq.cljs$core$IFn$_invoke$arity$3(self__.priority__GT_set_of_items,cljs.core._LT__EQ_,k));
if(cljs.core.truth_(self__.keyfn)){
return cljs.core.seq((function (){var iter__6925__auto__ = ((function (sets,this$__$1){
return (function tailrecursion$priority_map$iter__46826(s__46827){
return (new cljs.core.LazySeq(null,((function (sets,this$__$1){
return (function (){
var s__46827__$1 = s__46827;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__46827__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var vec__46836 = cljs.core.first(xs__5205__auto__);
var priority = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46836,(0),null);
var item_set = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46836,(1),null);
var iterys__6921__auto__ = ((function (s__46827__$1,vec__46836,priority,item_set,xs__5205__auto__,temp__4657__auto__,sets,this$__$1){
return (function tailrecursion$priority_map$iter__46826_$_iter__46828(s__46829){
return (new cljs.core.LazySeq(null,((function (s__46827__$1,vec__46836,priority,item_set,xs__5205__auto__,temp__4657__auto__,sets,this$__$1){
return (function (){
var s__46829__$1 = s__46829;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__46829__$1);
if(temp__4657__auto____$1){
var s__46829__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__46829__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__46829__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__46831 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__46830 = (0);
while(true){
if((i__46830 < size__6924__auto__)){
var item = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__46830);
cljs.core.chunk_append(b__46831,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,(self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1 ? self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1(item) : self__.item__GT_priority.call(null,item))], null));

var G__46862 = (i__46830 + (1));
i__46830 = G__46862;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__46831),tailrecursion$priority_map$iter__46826_$_iter__46828(cljs.core.chunk_rest(s__46829__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__46831),null);
}
} else {
var item = cljs.core.first(s__46829__$2);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,(self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1 ? self__.item__GT_priority.cljs$core$IFn$_invoke$arity$1(item) : self__.item__GT_priority.call(null,item))], null),tailrecursion$priority_map$iter__46826_$_iter__46828(cljs.core.rest(s__46829__$2)));
}
} else {
return null;
}
break;
}
});})(s__46827__$1,vec__46836,priority,item_set,xs__5205__auto__,temp__4657__auto__,sets,this$__$1))
,null,null));
});})(s__46827__$1,vec__46836,priority,item_set,xs__5205__auto__,temp__4657__auto__,sets,this$__$1))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(item_set));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,tailrecursion$priority_map$iter__46826(cljs.core.rest(s__46827__$1)));
} else {
var G__46863 = cljs.core.rest(s__46827__$1);
s__46827__$1 = G__46863;
continue;
}
} else {
return null;
}
break;
}
});})(sets,this$__$1))
,null,null));
});})(sets,this$__$1))
;
return iter__6925__auto__(sets);
})());
} else {
return cljs.core.seq((function (){var iter__6925__auto__ = ((function (sets,this$__$1){
return (function tailrecursion$priority_map$iter__46839(s__46840){
return (new cljs.core.LazySeq(null,((function (sets,this$__$1){
return (function (){
var s__46840__$1 = s__46840;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__46840__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var vec__46849 = cljs.core.first(xs__5205__auto__);
var priority = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46849,(0),null);
var item_set = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46849,(1),null);
var iterys__6921__auto__ = ((function (s__46840__$1,vec__46849,priority,item_set,xs__5205__auto__,temp__4657__auto__,sets,this$__$1){
return (function tailrecursion$priority_map$iter__46839_$_iter__46841(s__46842){
return (new cljs.core.LazySeq(null,((function (s__46840__$1,vec__46849,priority,item_set,xs__5205__auto__,temp__4657__auto__,sets,this$__$1){
return (function (){
var s__46842__$1 = s__46842;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__46842__$1);
if(temp__4657__auto____$1){
var s__46842__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__46842__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__46842__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__46844 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__46843 = (0);
while(true){
if((i__46843 < size__6924__auto__)){
var item = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__46843);
cljs.core.chunk_append(b__46844,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,priority], null));

var G__46864 = (i__46843 + (1));
i__46843 = G__46864;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__46844),tailrecursion$priority_map$iter__46839_$_iter__46841(cljs.core.chunk_rest(s__46842__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__46844),null);
}
} else {
var item = cljs.core.first(s__46842__$2);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [item,priority], null),tailrecursion$priority_map$iter__46839_$_iter__46841(cljs.core.rest(s__46842__$2)));
}
} else {
return null;
}
break;
}
});})(s__46840__$1,vec__46849,priority,item_set,xs__5205__auto__,temp__4657__auto__,sets,this$__$1))
,null,null));
});})(s__46840__$1,vec__46849,priority,item_set,xs__5205__auto__,temp__4657__auto__,sets,this$__$1))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(item_set));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,tailrecursion$priority_map$iter__46839(cljs.core.rest(s__46840__$1)));
} else {
var G__46865 = cljs.core.rest(s__46840__$1);
s__46840__$1 = G__46865;
continue;
}
} else {
return null;
}
break;
}
});})(sets,this$__$1))
,null,null));
});})(sets,this$__$1))
;
return iter__6925__auto__(sets);
})());
}
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$ISorted$_entry_key$arity$2 = (function (this$,entry){
var self__ = this;
var this$__$1 = this;
var G__46852 = cljs.core.val(entry);
return (self__.keyfn.cljs$core$IFn$_invoke$arity$1 ? self__.keyfn.cljs$core$IFn$_invoke$arity$1(G__46852) : self__.keyfn.call(null,G__46852));
});

tailrecursion.priority_map.PersistentPriorityMap.prototype.cljs$core$ISorted$_comparator$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
return cljs.core.compare;
});

tailrecursion.priority_map.PersistentPriorityMap.getBasis = (function (){
return new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$priority_DASH__GT_set_DASH_of_DASH_items,cljs.core.cst$sym$item_DASH__GT_priority,cljs.core.cst$sym$meta,cljs.core.cst$sym$keyfn,cljs.core.with_meta(cljs.core.cst$sym$__hash,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$mutable,true], null))], null);
});

tailrecursion.priority_map.PersistentPriorityMap.cljs$lang$type = true;

tailrecursion.priority_map.PersistentPriorityMap.cljs$lang$ctorStr = "tailrecursion.priority-map/PersistentPriorityMap";

tailrecursion.priority_map.PersistentPriorityMap.cljs$lang$ctorPrWriter = (function (this__6751__auto__,writer__6752__auto__,opt__6753__auto__){
return cljs.core._write(writer__6752__auto__,"tailrecursion.priority-map/PersistentPriorityMap");
});

tailrecursion.priority_map.__GT_PersistentPriorityMap = (function tailrecursion$priority_map$__GT_PersistentPriorityMap(priority__GT_set_of_items,item__GT_priority,meta,keyfn,__hash){
return (new tailrecursion.priority_map.PersistentPriorityMap(priority__GT_set_of_items,item__GT_priority,meta,keyfn,__hash));
});

tailrecursion.priority_map.PersistentPriorityMap.EMPTY = (new tailrecursion.priority_map.PersistentPriorityMap(cljs.core.sorted_map(),cljs.core.PersistentArrayMap.EMPTY,cljs.core.PersistentArrayMap.EMPTY,cljs.core.identity,null));
tailrecursion.priority_map.pm_empty_by = (function tailrecursion$priority_map$pm_empty_by(comparator){
return (new tailrecursion.priority_map.PersistentPriorityMap(cljs.core.sorted_map_by(comparator),cljs.core.PersistentArrayMap.EMPTY,cljs.core.PersistentArrayMap.EMPTY,cljs.core.identity,null));
});
tailrecursion.priority_map.pm_empty_keyfn = (function tailrecursion$priority_map$pm_empty_keyfn(var_args){
var args46866 = [];
var len__7211__auto___46869 = arguments.length;
var i__7212__auto___46870 = (0);
while(true){
if((i__7212__auto___46870 < len__7211__auto___46869)){
args46866.push((arguments[i__7212__auto___46870]));

var G__46871 = (i__7212__auto___46870 + (1));
i__7212__auto___46870 = G__46871;
continue;
} else {
}
break;
}

var G__46868 = args46866.length;
switch (G__46868) {
case 1:
return tailrecursion.priority_map.pm_empty_keyfn.cljs$core$IFn$_invoke$arity$1((arguments[(0)]));

break;
case 2:
return tailrecursion.priority_map.pm_empty_keyfn.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args46866.length)].join('')));

}
});

tailrecursion.priority_map.pm_empty_keyfn.cljs$core$IFn$_invoke$arity$1 = (function (keyfn){
return (new tailrecursion.priority_map.PersistentPriorityMap(cljs.core.sorted_map(),cljs.core.PersistentArrayMap.EMPTY,cljs.core.PersistentArrayMap.EMPTY,keyfn,null));
});

tailrecursion.priority_map.pm_empty_keyfn.cljs$core$IFn$_invoke$arity$2 = (function (keyfn,comparator){
return (new tailrecursion.priority_map.PersistentPriorityMap(cljs.core.sorted_map_by(comparator),cljs.core.PersistentArrayMap.EMPTY,cljs.core.PersistentArrayMap.EMPTY,keyfn,null));
});

tailrecursion.priority_map.pm_empty_keyfn.cljs$lang$maxFixedArity = 2;
tailrecursion.priority_map.read_priority_map = (function tailrecursion$priority_map$read_priority_map(elems){
if(cljs.core.map_QMARK_(elems)){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(tailrecursion.priority_map.PersistentPriorityMap.EMPTY,elems);
} else {
return cljs.reader.reader_error.cljs$core$IFn$_invoke$arity$variadic(null,cljs.core.array_seq(["Priority map literal expects a map for its elements."], 0));
}
});
cljs.reader.register_tag_parser_BANG_("tailrecursion.priority-map",tailrecursion.priority_map.read_priority_map);
/**
 * keyval => key val
 *   Returns a new priority map with supplied mappings.
 */
tailrecursion.priority_map.priority_map = (function tailrecursion$priority_map$priority_map(var_args){
var args__7218__auto__ = [];
var len__7211__auto___46874 = arguments.length;
var i__7212__auto___46875 = (0);
while(true){
if((i__7212__auto___46875 < len__7211__auto___46874)){
args__7218__auto__.push((arguments[i__7212__auto___46875]));

var G__46876 = (i__7212__auto___46875 + (1));
i__7212__auto___46875 = G__46876;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((0) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((0)),(0))):null);
return tailrecursion.priority_map.priority_map.cljs$core$IFn$_invoke$arity$variadic(argseq__7219__auto__);
});

tailrecursion.priority_map.priority_map.cljs$core$IFn$_invoke$arity$variadic = (function (keyvals){
var in$ = cljs.core.seq(keyvals);
var out = tailrecursion.priority_map.PersistentPriorityMap.EMPTY;
while(true){
if(in$){
var G__46877 = cljs.core.nnext(in$);
var G__46878 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(out,cljs.core.first(in$),cljs.core.second(in$));
in$ = G__46877;
out = G__46878;
continue;
} else {
return out;
}
break;
}
});

tailrecursion.priority_map.priority_map.cljs$lang$maxFixedArity = (0);

tailrecursion.priority_map.priority_map.cljs$lang$applyTo = (function (seq46873){
return tailrecursion.priority_map.priority_map.cljs$core$IFn$_invoke$arity$variadic(cljs.core.seq(seq46873));
});
/**
 * keyval => key val
 *   Returns a new priority map with supplied
 *   mappings, using the supplied comparator.
 */
tailrecursion.priority_map.priority_map_by = (function tailrecursion$priority_map$priority_map_by(var_args){
var args__7218__auto__ = [];
var len__7211__auto___46881 = arguments.length;
var i__7212__auto___46882 = (0);
while(true){
if((i__7212__auto___46882 < len__7211__auto___46881)){
args__7218__auto__.push((arguments[i__7212__auto___46882]));

var G__46883 = (i__7212__auto___46882 + (1));
i__7212__auto___46882 = G__46883;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return tailrecursion.priority_map.priority_map_by.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

tailrecursion.priority_map.priority_map_by.cljs$core$IFn$_invoke$arity$variadic = (function (comparator,keyvals){
var in$ = cljs.core.seq(keyvals);
var out = tailrecursion.priority_map.pm_empty_by(comparator);
while(true){
if(in$){
var G__46884 = cljs.core.nnext(in$);
var G__46885 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(out,cljs.core.first(in$),cljs.core.second(in$));
in$ = G__46884;
out = G__46885;
continue;
} else {
return out;
}
break;
}
});

tailrecursion.priority_map.priority_map_by.cljs$lang$maxFixedArity = (1);

tailrecursion.priority_map.priority_map_by.cljs$lang$applyTo = (function (seq46879){
var G__46880 = cljs.core.first(seq46879);
var seq46879__$1 = cljs.core.next(seq46879);
return tailrecursion.priority_map.priority_map_by.cljs$core$IFn$_invoke$arity$variadic(G__46880,seq46879__$1);
});
/**
 * keyval => key val
 *   Returns a new priority map with supplied
 *   mappings, using the supplied keyfn.
 */
tailrecursion.priority_map.priority_map_keyfn = (function tailrecursion$priority_map$priority_map_keyfn(var_args){
var args__7218__auto__ = [];
var len__7211__auto___46888 = arguments.length;
var i__7212__auto___46889 = (0);
while(true){
if((i__7212__auto___46889 < len__7211__auto___46888)){
args__7218__auto__.push((arguments[i__7212__auto___46889]));

var G__46890 = (i__7212__auto___46889 + (1));
i__7212__auto___46889 = G__46890;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return tailrecursion.priority_map.priority_map_keyfn.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

tailrecursion.priority_map.priority_map_keyfn.cljs$core$IFn$_invoke$arity$variadic = (function (keyfn,keyvals){
var in$ = cljs.core.seq(keyvals);
var out = tailrecursion.priority_map.pm_empty_keyfn.cljs$core$IFn$_invoke$arity$1(keyfn);
while(true){
if(in$){
var G__46891 = cljs.core.nnext(in$);
var G__46892 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(out,cljs.core.first(in$),cljs.core.second(in$));
in$ = G__46891;
out = G__46892;
continue;
} else {
return out;
}
break;
}
});

tailrecursion.priority_map.priority_map_keyfn.cljs$lang$maxFixedArity = (1);

tailrecursion.priority_map.priority_map_keyfn.cljs$lang$applyTo = (function (seq46886){
var G__46887 = cljs.core.first(seq46886);
var seq46886__$1 = cljs.core.next(seq46886);
return tailrecursion.priority_map.priority_map_keyfn.cljs$core$IFn$_invoke$arity$variadic(G__46887,seq46886__$1);
});
/**
 * keyval => key val
 *   Returns a new priority map with supplied
 *   mappings, using the supplied keyfn and comparator.
 */
tailrecursion.priority_map.priority_map_keyfn_by = (function tailrecursion$priority_map$priority_map_keyfn_by(var_args){
var args__7218__auto__ = [];
var len__7211__auto___46896 = arguments.length;
var i__7212__auto___46897 = (0);
while(true){
if((i__7212__auto___46897 < len__7211__auto___46896)){
args__7218__auto__.push((arguments[i__7212__auto___46897]));

var G__46898 = (i__7212__auto___46897 + (1));
i__7212__auto___46897 = G__46898;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((2) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((2)),(0))):null);
return tailrecursion.priority_map.priority_map_keyfn_by.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),(arguments[(1)]),argseq__7219__auto__);
});

tailrecursion.priority_map.priority_map_keyfn_by.cljs$core$IFn$_invoke$arity$variadic = (function (keyfn,comparator,keyvals){
var in$ = cljs.core.seq(keyvals);
var out = tailrecursion.priority_map.pm_empty_keyfn.cljs$core$IFn$_invoke$arity$2(keyfn,comparator);
while(true){
if(in$){
var G__46899 = cljs.core.nnext(in$);
var G__46900 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(out,cljs.core.first(in$),cljs.core.second(in$));
in$ = G__46899;
out = G__46900;
continue;
} else {
return out;
}
break;
}
});

tailrecursion.priority_map.priority_map_keyfn_by.cljs$lang$maxFixedArity = (2);

tailrecursion.priority_map.priority_map_keyfn_by.cljs$lang$applyTo = (function (seq46893){
var G__46894 = cljs.core.first(seq46893);
var seq46893__$1 = cljs.core.next(seq46893);
var G__46895 = cljs.core.first(seq46893__$1);
var seq46893__$2 = cljs.core.next(seq46893__$1);
return tailrecursion.priority_map.priority_map_keyfn_by.cljs$core$IFn$_invoke$arity$variadic(G__46894,G__46895,seq46893__$2);
});
