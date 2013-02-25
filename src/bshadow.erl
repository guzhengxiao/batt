-module( bshadow ).
-export([start/0, init/0 , store/2 , fetch/1, fold/2]).

start()->
    application:start(bshadow).

% record { time ,  msg , receive_time }
init() -> 
    case ets:info(?MODULE) of
        undefined -> ets:new(?MODULE , [named_table , duplicate_bag , public])
        ;_ -> ok
    end
    ,ok.

store( Time , Msg ) when is_integer(Time) ->
    ets:insert(?MODULE , { Time , term_to_binary( Msg ) , bshadow_timer:now() })
;store( _ , _  ) -> badargs.

fetch( Time ) when is_integer(Time) ->
    case ets:lookup(?MODULE ,  Time  ) of
        [{Time,undefined,0}] -> []
        ;A -> A
    end
;fetch(_) -> badargs.

fold( Start , Len ) when is_integer(Start) andalso is_integer(Len) ->
    ets:insert_new(?MODULE , {Start , undefined,0} )
    ,fold( Start ,Len ,[] )
;fold( _ , _ ) -> badargs.
    
fold(K , L , R) when K =:= '$end_of_table' orelse L =< 0 ->
    R
;fold(K , L , R) -> 
    case ets:lookup( ?MODULE, K ) of
        [] -> fold( ets:next( ?MODULE , K ) , L , R)
        ;[{_ , undefined,0}] -> fold( ets:next(?MODULE , K ) , L,R)
        ;V -> fold( ets:next(?MODULE , K) , L -1 , R++V )
    end.

%do( N ,M , F , A ) ->
%    rpc:call( N , bnow , eval , [  ]  )
%    ,apply( M , F , A ).
