"""
Traducciones para el AI Coach
Mensajes en Español, Inglés y Francés
"""

TRANSLATIONS = {
 'Español': {
 'motivation_low': [
 "¡Vamos {name}! Estás comenzando fuerte. ¡Cada paso cuenta!",
 "¡Excelente inicio, {name}! Tu cuerpo te lo agradecerá.",
 "¡Así se hace, {name}! Estás construyendo un mejor tú."
 ],
 'motivation_mid': [
 "¡Increíble, {name}! Ya llevas {percent:.0f}%. ¡No pares ahora! ",
 "¡Vas por buen camino, {name}! {percent:.0f}% completado. ¡Tú puedes! ",
 "¡Mitad del camino, {name}! {calories:.0f} calorías eliminadas. ¡Sigue así! "
 ],
 'motivation_high': [
 "¡Wow {name}! Ya {percent:.0f}% completado. ¡Estás imparable! ",
 "¡Fantástico, {name}! {calories:.0f} kcal quemadas. ¡La meta está cerca! ",
 "¡Brutal, {name}! Ya casi llegas. ¡No te detengas ahora! "
 ],
 'motivation_veryhigh': [
 "¡CASI LO LOGRAS, {name}! {percent:.0f}% ¡El último empujón! ",
 "¡ERES INCREÍBLE, {name}! Solo falta {remaining:.0f} kcal. ¡VAMOS! ",
 "¡LA VICTORIA ESTÁ CERCA, {name}! {percent:.0f}% ¡TÚ PUEDES! "
 ],
 'progress': [
 " Progreso actual: {calories:.0f} kcal ({percent:.1f}%). ¡Sigue adelante, {name}!",
 " Llevas {calories:.0f} calorías quemadas. ¡Eso es {percent:.1f}% del objetivo!",
 " {name}, has eliminado {calories:.0f} kcal. ¡{percent:.1f}% completado!"
 ],
 'nutrition': [
 " Hidratación: Bebe agua para recuperarte. Has perdido mucho líquido.",
 " Post-entrenamiento: Considera proteína + carbohidratos en los próximos 30 min.",
 " Recuperación: Un plátano y frutos secos son perfectos ahora.",
 " Rehidratación: Agua con electrolitos ayudará a tu recuperación.",
 " Proteína: Un batido de proteína optimizará tu recuperación muscular.",
 " Grasas saludables: Aguacate o nueces ayudan a la recuperación."
 ],
 'wellness': [
 " {name}, la felicidad está en los pequeños logros diarios. Celebra cada victoria.",
 " Cada día es una nueva oportunidad, {name}. Disfruta el proceso, no solo el resultado.",
 " Tu salud mental es tan importante como la física. Descansa cuando lo necesites.",
 " {name}, la consistencia supera la perfección. Pequeños pasos todos los días.",
 " El equilibrio es clave: ejercicio, nutrición, descanso y alegría.",
 " {name}, cada entrenamiento es una inversión en tu futuro yo. ¡Sigue adelante!",
 " Define metas, pero disfruta el camino. La vida es el viaje, no el destino.",
 " Tu cuerpo es tu templo, {name}. Cuídalo con amor y respeto."
 ],
 'food_comparison_exceeded': "¡{name}! Has quemado el equivalente a {food} ({food_cals} kcal). ¡Sigue así!",
 'food_comparison_progress': "Ya llevas el {percent:.0f}% de {food}. ¡Continúa, {name}!",
 'food_comparison_default': "¡Vas muy bien, {name}! Cada caloría cuenta.",
 'congratulations': "¡Felicidades {name}! Has completado tu entrenamiento. ¡Eres increíble!"
 },
 'English': {
 'motivation_low': [
 "Let's go {name}! You're starting strong. Every step counts!",
 "Excellent start, {name}! Your body will thank you.",
 "That's how it's done, {name}! You're building a better you."
 ],
 'motivation_mid': [
 "Amazing, {name}! You're at {percent:.0f}%. Don't stop now! ",
 "You're on the right track, {name}! {percent:.0f}% completed. You can do it! ",
 "Halfway there, {name}! {calories:.0f} calories burned. Keep it up! "
 ],
 'motivation_high': [
 "Wow {name}! Already {percent:.0f}% complete. You're unstoppable! ",
 "Fantastic, {name}! {calories:.0f} kcal burned. The goal is near! ",
 "Awesome, {name}! Almost there. Don't stop now! "
 ],
 'motivation_veryhigh': [
 "ALMOST THERE, {name}! {percent:.0f}% The final push! ",
 "YOU'RE INCREDIBLE, {name}! Only {remaining:.0f} kcal left. LET'S GO! ",
 "VICTORY IS NEAR, {name}! {percent:.0f}% YOU CAN DO IT! "
 ],
 'progress': [
 " Current progress: {calories:.0f} kcal ({percent:.1f}%). Keep going, {name}!",
 " You've burned {calories:.0f} calories. That's {percent:.1f}% of your goal!",
 " {name}, you've eliminated {calories:.0f} kcal. {percent:.1f}% complete!"
 ],
 'nutrition': [
 " Hydration: Drink water to recover. You've lost a lot of fluids.",
 " Post-workout: Consider protein + carbs in the next 30 min.",
 " Recovery: A banana and nuts are perfect right now.",
 " Rehydration: Water with electrolytes will help your recovery.",
 " Protein: A protein shake will optimize your muscle recovery.",
 " Healthy fats: Avocado or nuts help with recovery."
 ],
 'wellness': [
 " {name}, happiness is in the small daily achievements. Celebrate every victory.",
 " Every day is a new opportunity, {name}. Enjoy the process, not just the result.",
 " Your mental health is as important as physical. Rest when you need it.",
 " {name}, consistency beats perfection. Small steps every day.",
 " Balance is key: exercise, nutrition, rest, and joy.",
 " {name}, every workout is an investment in your future self. Keep going!",
 " Set goals, but enjoy the journey. Life is the journey, not the destination.",
 " Your body is your temple, {name}. Take care of it with love and respect."
 ],
 'food_comparison_exceeded': "{name}! You've burned the equivalent of {food} ({food_cals} kcal). Keep it up!",
 'food_comparison_progress': "You're at {percent:.0f}% of {food}. Keep going, {name}!",
 'food_comparison_default': "You're doing great, {name}! Every calorie counts.",
 'congratulations': "Congratulations {name}! You've completed your workout. You're amazing!"
 },
 'Français': {
 'motivation_low': [
 "Allez {name}! Tu commences fort. Chaque pas compte!",
 "Excellent début, {name}! Ton corps te remerciera.",
 "C'est comme ça, {name}! Tu construis un meilleur toi."
 ],
 'motivation_mid': [
 "Incroyable, {name}! Tu es à {percent:.0f}%. Ne t'arrête pas! ",
 "Tu es sur la bonne voie, {name}! {percent:.0f}% complété. Tu peux le faire! ",
 "À mi-chemin, {name}! {calories:.0f} calories brûlées. Continue! "
 ],
 'motivation_high': [
 "Wow {name}! Déjà {percent:.0f}% terminé. Tu es inarrêtable! ",
 "Fantastique, {name}! {calories:.0f} kcal brûlées. L'objectif est proche! ",
 "Génial, {name}! Presque là. Ne t'arrête pas! "
 ],
 'motivation_veryhigh': [
 "PRESQUE RÉUSSI, {name}! {percent:.0f}% Le dernier effort! ",
 "TU ES INCROYABLE, {name}! Seulement {remaining:.0f} kcal restantes. ALLEZ! ",
 "LA VICTOIRE EST PROCHE, {name}! {percent:.0f}% TU PEUX LE FAIRE! "
 ],
 'progress': [
 " Progrès actuel: {calories:.0f} kcal ({percent:.1f}%). Continue, {name}!",
 " Tu as brûlé {calories:.0f} calories. C'est {percent:.1f}% de ton objectif!",
 " {name}, tu as éliminé {calories:.0f} kcal. {percent:.1f}% complété!"
 ],
 'nutrition': [
 " Hydratation: Bois de l'eau pour récupérer. Tu as perdu beaucoup de liquide.",
 " Post-entraînement: Considère protéine + glucides dans les 30 prochaines min.",
 " Récupération: Une banane et des noix sont parfaites maintenant.",
 " Réhydratation: L'eau avec électrolytes aidera ta récupération.",
 " Protéine: Un shake protéiné optimisera ta récupération musculaire.",
 " Graisses saines: Avocat ou noix aident à la récupération."
 ],
 'wellness': [
 " {name}, le bonheur est dans les petites réussites quotidiennes. Célèbre chaque victoire.",
 " Chaque jour est une nouvelle opportunité, {name}. Profite du processus, pas seulement du résultat.",
 " Ta santé mentale est aussi importante que la physique. Repose-toi quand tu en as besoin.",
 " {name}, la constance bat la perfection. Petits pas chaque jour.",
 " L'équilibre est la clé: exercice, nutrition, repos et joie.",
 " {name}, chaque entraînement est un investissement dans ton futur. Continue!",
 " Définis des objectifs, mais profite du voyage. La vie est le voyage, pas la destination.",
 " Ton corps est ton temple, {name}. Prends-en soin avec amour et respect."
 ],
 'food_comparison_exceeded': "{name}! Tu as brûlé l'équivalent de {food} ({food_cals} kcal). Continue!",
 'food_comparison_progress': "Tu es à {percent:.0f}% de {food}. Continue, {name}!",
 'food_comparison_default': "Tu vas très bien, {name}! Chaque calorie compte.",
 'congratulations': "Félicitations {name}! Tu as terminé ton entraînement. Tu es incroyable!"
 }
}
