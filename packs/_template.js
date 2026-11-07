// HOW TO ADD A NEW EXPANSION PACK
// 1. Copy this file to packs/<your-id>.js and fill it in.
// 2. Add one line to index.html, next to the other packs:
//      <script src="packs/<your-id>.js"></script>
// 3. Add 'packs/<your-id>.js', to the FILES list in sw.js and change VERSION there.
// 4. Reload. The pack appears in "Choose your industry".
//
// Card effects are [cash, morale, compliance, reputation], usually between -25 and +25.
// Put `law:'...'` on the risky option to teach the rule in the debrief.
// Optional on a card: once:1 (show only once), next:['card_id', weeksLater] (story follow-up, the follow-up card needs req:1),
// bias:'age'|'origin'|'parent'|'language'|'disability'|'gender' (flags a hiring-bias pattern).
// Give every card id the pack's prefix so it never clashes with another pack.
registerPack({
 id:'yourpack',icon:'🏷️',name:'Your Industry, Town',tagline:'One funny line about this world',
 i18n:{ms:{name:'',tagline:''},zh:{name:'',tagline:''},ta:{name:'',tagline:''}},
 people:{
  yp_lead:{n:'Name',r:'Role',e:'🙂',c:'#e6e6e6',bio:'One line that makes them memorable.'},
 },
 introCard:{id:'yp_intro',p:'yp_lead',once:1,t:'Welcome line that sets the scene.',
  L:{l:'Left choice',e:[0,0,0,0]},R:{l:'Right choice',e:[0,0,0,0]}},
 cards:[
  {id:'yp_example',p:'yp_lead',t:'The situation, in the character\'s own voice.',
   L:{l:'Risky shortcut',e:[10,-10,-15,0],law:'What the law actually says.'},
   R:{l:'The fair option',e:[-10,10,10,0]}},
 ]});
