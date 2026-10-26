type Tick = {symbol:string;price:number;volume:number};
class MarketPulse {
  private events: Tick[]=[];
  append(event:Tick):void {this.events.push(event)}
  bursts():number {return this.events.filter(e=>e.volume>1000).length}
}
