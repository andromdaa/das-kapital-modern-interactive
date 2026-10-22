"""Merge slice candidates (work/theme-slices/slice-N.json) into themes-index.json and themes-index.md.

Each merged item lists its source candidates ("slice.index"); anchors are the union of the sources'
anchors unless overridden. Quotes are taken from one source and verified against original/.
"""
import json, re, unicodedata
from pathlib import Path

root = Path(__file__).resolve().parent.parent
cands = {}
for n in range(1, 9):
    for i, x in enumerate(json.loads((root / f"work/theme-slices/slice-{n}.json").read_text())):
        cands[f"{n}.{i}"] = x
anchors = json.loads((root / "anchors.json").read_text())

D, W, F = "described_pattern", "general_warning", "concrete_forecast"

# (title, kind, specificity, testable, sources, claim, quote_source, note)
# kind: theme | forecast | implicit_argument. Speaker is Marx unless note says otherwise.
ITEMS = [
 ("Value is set by socially necessary labor time", "theme", D, "no", ["1.0", "1.1", "1.2", "2.11", "2.3", "2.23", "6.7"],
  "A commodity's value is the labor time socially necessary to produce it under average conditions; labor has a concrete side (making useful things) and an abstract side (forming value). Surplus-value comes from labor-power producing more value than it costs, not from exchange, and its rate is surplus labor over necessary labor.",
  "1.0", "The book's core definitions. Treated as an analytical framework, not an empirical forecast."),
 ("Commodity fetishism: social relations appear as relations between things", "theme", D, "no", ["1.3", "4.1", "3.10"],
  "Under commodity production, relations between producers show up as prices and values that seem to belong to things and to rule people. The productive power of co-operating workers likewise appears as a natural power of capital.",
  "1.3", ""),
 ("Economic categories are historical, not natural", "theme", D, "no", ["1.4", "1.18", "1.17", "1.19"],
  "Value, wages, and capital belong to one historically specific mode of production, though economists treat them as eternal. The economic structure is the basis on which legal, political, and religious life rests; religion's mystification can vanish only when social relations become transparent under consciously planned, freely associated production.",
  "1.4", "Includes the claims that Protestantism suits commodity society and that religion will fade under transparent social relations; both too general to test."),
 ("Rising productivity: more goods, less value per unit", "implicit_argument", D, "yes", ["1.6", "1.7", "4.0", "4.6"],
  "Value per unit varies inversely with productivity, so material wealth can grow while value per item falls; a new technique that halves the labor needed devalues the output of producers still using the old method, however hard they work. Capital has a constant drive to raise productivity, cheapening workers' necessities and so the worker.",
  "1.6", ""),
 ("Money must be a commodity with its own value", "implicit_argument", W, "yes", ["1.8", "2.21", "1.5"],
  "Money is by nature a commodity (gold, silver) whose value is real and set by labor time; it is not a convention or mere symbol. Inconvertible state paper issued beyond the gold that would otherwise circulate simply represents less gold, so prices rise in proportion.",
  "1.8", "Marx states the paper-money rule for paper standing in for gold and sets credit money aside (ch03-p067)."),
 ("Abolishing money while keeping commodity production is utopian", "implicit_argument", W, "yes", ["1.9"],
  "Schemes that keep private commodity production but abolish money or make all commodities directly exchangeable (Proudhon, Gray, Bray's labor-money) are incoherent; Owen's labor certificates work only because they presuppose a directly associated community.",
  "1.9", ""),
 ("Exchange begins at the edges of communities", "implicit_argument", D, "yes", ["1.10"],
  "Commodity exchange first arises between communities, not within them; once products become commodities externally, they become so internally too. Nomadic peoples first develop the money form.",
  "1.10", "A historical-anthropological claim about the origin of exchange."),
 ("Crises are possible because sale and purchase can come apart", "implicit_argument", D, "yes", ["1.11", "2.20", "2.16"],
  "Money lets a sale happen without an immediate purchase, so the unity of sale and purchase can reassert itself violently in a crisis. When long chains of payments break, credit money suddenly fails and everyone demands hard cash: money becomes the only wealth. Marx says these show only the possibility of crises; their actual causes come later.",
  "2.20", ""),
 ("The law of value works through chaotic fluctuation", "theme", D, "no", ["1.12", "1.13"],
  "Whether private labor counted as socially necessary is decided only after the fact on the market; price fluctuations and periodic upheavals are how the regulating law of value asserts itself, like gravity when a house falls.",
  "1.13", ""),
 ("Money makes everything saleable, even things that are not products", "implicit_argument", W, "yes", ["1.14", "2.22"],
  "Things that are not products of labor, such as conscience and honor, can take a price, and price can exist without value (uncultivated land). Money dissolves distinctions and turns social power into the private power of private persons.",
  "2.22", "Broad; testable only as a claim about the extent of commodification."),
 ("The quantity of money follows prices, not the reverse", "implicit_argument", D, "yes", ["1.15"],
  "The amount of money circulating equals the sum of prices divided by its velocity; prices are not set by the quantity of money. The common belief that stagnation comes from too little money is a delusion, though bad legislation on the currency can cause trouble too.",
  "1.15", "Stated for a metallic currency. The opposing quantity theory is listed as O03."),
 ("Two metals cannot both serve as the standard of value", "implicit_argument", D, "yes", ["1.16"],
  "Where gold and silver are both legal standards, shifts in their relative value disturb prices and in practice only one metal serves; the undervalued metal leaves circulation.",
  "1.16", ""),
 ("Silver will lose its role as world money (Engels's note)", "forecast", F, "yes", ["2.18"],
  "Silver's value will keep falling for a long time, hopes of restoring the old gold-silver ratio are utopian, and silver will increasingly lose its money function in world markets.",
  "2.18", "Speaker: Engels, in a note added to the 4th German edition, not Marx's own text."),
 ("Credit money displaces coin; hoarding fades", "forecast", W, "yes", ["2.19"],
  "Hoarding as a way of getting rich fades as bourgeois society progresses, while reserves held for payments grow; credit money comes to dominate large-scale commerce and metal coin is pushed into retail trade.",
  "2.19", ""),
 ("Foreign trade will sweep away Japan's model agriculture", "forecast", F, "yes", ["2.17"],
  "If trade forced on Japan by Europeans brings money rents in place of rents in kind, Japan's exemplary agriculture, which rests on narrow economic conditions, will be swept away.",
  "2.17", "Conditional ('if'), written in the 1860s."),
 ("Capital as self-expanding value with no natural limit", "theme", D, "no", ["2.0", "2.1", "2.6"],
  "Capital is money advanced to return as more money (M-C-M'); because its aim is quantitative, the process has no natural end. The capitalist functions as capital personified, aiming at endless profit-making rather than any single gain or use.",
  "2.0", ""),
 ("Competition compels endless accumulation", "implicit_argument", D, "yes", ["7.0", "7.1", "6.22"],
  "Competition imposes capitalism's laws on each capitalist as external pressure, forcing him to keep expanding capital to keep it: 'production for production's sake'. The more already accumulated, the more can be accumulated. This develops productive forces that could be the basis of a higher society.",
  "7.0", "The 'higher society' clause (ch24-p048) is too general to test; the reinvestment compulsion is testable."),
 ("Wage labor needs workers 'free' of both bosses and property", "implicit_argument", D, "yes", ["2.7", "8.0", "8.1", "8.2", "8.3", "8.4", "8.8", "8.9"],
  "Capital needs workers free to sell their labor-power and free of any means of production. This condition is not natural but the product of history: in England, the expropriation of the peasantry through enclosure (increasingly by Act of Parliament), clearances, and seizure of church and Crown lands, which also created the home market by destroying rural domestic industry.",
  "8.2", "Historical thesis. Marx sets 'purely economic causes' aside and focuses on force; historians dispute the weight he gives each."),
 ("Wages include a 'historical and moral' element", "implicit_argument", D, "yes", ["2.8"],
  "The value of labor-power is the cost of the necessities to maintain and raise a worker's family, but what counts as necessary includes a historical and moral element that varies by country and by the habits the working class formed; below the physical minimum, workers survive only in a crippled state.",
  "2.8", ""),
 ("Workers lend to their employers by being paid in arrears", "implicit_argument", D, "yes", ["2.9"],
  "Because wages are paid after the work is done, the worker everywhere gives credit to the capitalist, and bears the losses: unpaid wages when employers go bankrupt, buying on credit at higher prices, truck shops, and adulterated goods.",
  "2.9", ""),
 ("Physical deterioration of the working class", "implicit_argument", D, "yes", ["2.14", "3.5", "4.13"],
  "Where hours are unrestricted, generations of workers are stunted, diseased and short-lived, kept going by recruits from the countryside; where capitalism is well developed, the working class's physique has deteriorated. Marx links this to falling military height standards in Germany and France, and says the division of labor in manufacture first gave material for industrial pathology.",
  "2.14", "Marx states it as a fact of his time; whether it continues is the testable part."),
 ("Unchecked, capital would wear out the workforce", "forecast", W, "yes", ["3.6", "3.7"],
  "Capital is indifferent to workers' lifespan unless society compels it to care; where replacements are plentiful (slave trade, or a labor market with surplus population), workers are used up. Left alone it points to the degradation and depopulation of the race; each capitalist hopes the crash will fall on his neighbor.",
  "3.6", "Explicitly conditional on the absence of social compulsion. The 'depopulation' phrase is rhetorical."),
 ("The length of the working day is settled by class struggle", "implicit_argument", D, "yes", ["3.0", "3.13", "3.16", "3.1"],
  "Exchange alone does not fix the working day; between buyer's and seller's equal rights, force decides. The isolated worker cannot resist, so workers must combine as a class to force a legal limit; a legal limit on the working day is the precondition of every further improvement.",
  "3.0", ""),
 ("Joining the world market intensifies forced labor", "implicit_argument", D, "yes", ["3.2"],
  "When slave or serf (corvée) production is drawn into a capitalist world market and turns to export, the 'civilized horrors of overwork' are grafted onto the older forms (cotton slavery in the American South, Danubian corvée).",
  "3.2", ""),
 ("Stealing minutes: unpaid time taken in small pieces", "implicit_argument", D, "yes", ["3.3"],
  "Where hours are legally limited, employers systematically nibble minutes from meal breaks and start and stop times; small individually, these add up to weeks of unpaid work per year and are hard for inspectors to prove.",
  "3.3", ""),
 ("In slumps, employers squeeze more from those still working", "implicit_argument", D, "yes", ["3.4"],
  "Downturns do not weaken the drive to extend hours: the less business there is, the more profit must be made on what remains, so overwork persists alongside short time.",
  "3.4", ""),
 ("Competition stops employers limiting hours voluntarily; they ask for uniform law", "implicit_argument", D, "yes", ["3.8", "5.20", "4.19"],
  "However humane, individual capitalists cannot shorten hours alone because competition compels them; firms therefore petition for legislation that binds all competitors equally. Capital, as a leveller, demands equal conditions in every branch, and resists even cheap health measures beyond a certain point unless a general law imposes them.",
  "3.8", ""),
 ("Capital pushes production around the clock", "implicit_argument", D, "yes", ["3.9"],
  "From capital's standpoint idle means of production are a loss, so there is an inherent tendency to run them 24 hours through night work and relay systems.",
  "3.9", ""),
 ("The worst exploitation is in scattered, unregulated work", "implicit_argument", D, "yes", ["3.11", "5.18"],
  "Capital takes the labor process as it finds it, so old trades and homework can be worse than factories. Modern 'domestic industry' is an outside department of the factory, and exploitation is most shameless there because workers' resistance falls as they are dispersed; once sweating reaches its limits, machinery and the factory take over.",
  "5.18", ""),
 ("Factory laws will spread to all industries and countries", "forecast", F, "yes", ["3.12", "6.0"],
  "Regulation began as an exception for textile mills but will be compelled to shed its exceptional character as capitalism takes over other trades; there is an irresistible tendency toward general application, already seen in France, Switzerland, Austria and the US eight-hour movement.",
  "6.0", "Marx notes agriculture, mines and transport were not yet covered, and that 'a reaction has again set in' since 1866."),
 ("Employers evade labor laws when enforcement is thin", "implicit_argument", D, "yes", ["3.14", "6.6"],
  "After the Ten Hours Act, manufacturers evaded the law through sham relay systems, legal technicalities and friendly magistrates; mining and workshop laws stayed largely dead letters because inspectors were few and workers feared reprisal.",
  "3.14", ""),
 ("Shorter hours raise output per hour and need not ruin industry", "implicit_argument", D, "yes", ["3.15", "5.4", "6.10"],
  "Experiments and inspectors' reports showed output in 10 or 11 hours matching that of 12; a shorter day spurs better machinery and harder work per hour, and the regulated industries flourished afterward.",
  "5.4", "Marx concedes the rate of surplus-value falls somewhat and that wage cuts followed (ch10-p160)."),
 ("Capital tends to cut the number of workers it employs", "forecast", W, "yes", ["3.17", "5.14", "7.10", "7.13", "5.12"],
  "Accumulation itself constantly produces a relatively redundant working population, in proportion to its energy. Machinery displaces workers and locks capital up in machines instead of freeing it to re-employ them; displaced workers find jobs elsewhere only through new capital, after a painful transition, and employment falls relative to capital and sometimes absolutely.",
  "7.10", "The opposing 'compensation theory' is O15."),
 ("The industrial reserve army regulates wages", "implicit_argument", D, "yes", ["7.11", "7.7", "7.15"],
  "A reserve of unemployed and underemployed workers (floating, latent rural, and stagnant irregular layers, with paupers at the bottom) is a condition of capitalist production: it supplies hands for sudden expansions and its swelling and shrinking, not absolute population, governs wages. Wages are the dependent variable; rises stop before they threaten accumulation.",
  "7.11", ""),
 ("Machinery deskills, replacing skilled with less skilled labor", "forecast", W, "yes", ["4.2", "4.11", "5.8", "4.12"],
  "The division of labor splits crafts into detail tasks and creates a class of 'unskilled' workers; machinery goes further, constantly replacing skilled men with less skilled hands. Knowledge and judgment are separated from the worker and concentrated in capital and in science made a productive force distinct from labor.",
  "5.8", ""),
 ("Anarchy in the market, despotism in the workplace", "theme", D, "no", ["4.3"],
  "Society's division of labor is coordinated only after the fact by exchange and competition, while within the workshop it is planned under the capitalist's authority; bourgeois thought praises the second and denounces any planning of the first.",
  "4.3", ""),
 ("The worker becomes an appendage of the machine", "implicit_argument", D, "yes", ["4.4", "5.6", "2.13"],
  "In the machine system the machine sets the pace and uses the worker rather than the reverse; skill passes into the machine, work is reduced to minding, and the worker faces barrack-like factory discipline and fines.",
  "5.6", ""),
 ("Productivity gains are not used to shorten the working day", "implicit_argument", W, "yes", ["4.7", "5.0", "6.11", "4.20"],
  "Capital aims to cut the labor time per product, not the worker's day; machinery, which could shorten labor, instead gives capital motives to lengthen it. Under capital the day can never shrink to only the necessary labor time.",
  "4.7", ""),
 ("Innovators' extra profit is temporary", "implicit_argument", D, "yes", ["4.8"],
  "A capitalist who adopts a better method earns extra surplus-value while his costs are below the social average, but this vanishes once the method spreads; competition compels rivals to adopt it.",
  "4.8", ""),
 ("Concentration and centralization of capital", "forecast", F, "yes", ["4.9", "7.9", "8.14", "5.17"],
  "The minimum capital needed to operate keeps rising; large capitals beat small ones; credit and joint-stock companies become powerful levers of centralization; one capitalist always kills many and the number of capital magnates constantly diminishes. The theoretical limit is all capital in one hand.",
  "8.14", "Marx also notes counter-tendencies (new capitals splitting off, ch25-p024). Engels's note on trusts (ch25) is his own addition."),
 ("Regulation speeds the concentration of capital", "forecast", F, "yes", ["6.1", "5.19"],
  "Legal limits on hours and conditions force more machinery and larger scale, ruin small masters and domestic industries, and so accelerate concentration and the dominance of the factory system.",
  "6.1", ""),
 ("Management becomes a separate hierarchy", "implicit_argument", D, "yes", ["4.10"],
  "As co-operation grows, the capitalist hands supervision to a special class of managers and foremen who command in capital's name; this control is both technical co-ordination and an instrument of exploitation, and workers' resistance grows with their numbers.",
  "4.10", ""),
 ("Machinery as a weapon against strikes and skilled workers", "implicit_argument", D, "yes", ["4.14", "5.9"],
  "Manufacture depended on skilled hands and so struggled with their insubordination; machinery removes that dependence, and since 1830 many inventions were made to break strikes.",
  "5.9", ""),
 ("A revolution in one industry forces revolutions in linked industries", "implicit_argument", D, "yes", ["4.15"],
  "A radical change in one branch (spinning) compels change in connected branches and revolutionizes transport and communication; modern industry must eventually build machines by machines.",
  "4.15", ""),
 ("Machinery draws women and children into paid work and dilutes the family wage", "implicit_argument", D, "yes", ["4.16", "4.17"],
  "Machinery makes muscular strength unnecessary, so capital recruits women and children; the value of the man's labor-power is spread across the family, more family members must work to live, and male workers' resistance is broken.",
  "4.16", ""),
 ("Machines are adopted only when cheaper than wages", "implicit_argument", D, "yes", ["4.18", "4.5"],
  "For the capitalist, a machine pays only if it costs less than the wages it replaces, not the labor it saves; so machines invented in high-wage countries go unused where labor is cheap, and labor laws can spur mechanization.",
  "4.18", ""),
 ("Hour limits lead to intensified work", "implicit_argument", D, "yes", ["5.2", "6.3"],
  "Once law fixes the working day, capital turns to intensity: faster machines, more machines per worker, and 'closer filling up of the pores' of the day.",
  "5.2", ""),
 ("Another cut in working hours will become inevitable", "forecast", F, "yes", ["5.3"],
  "Because capital converts every machine improvement into more exhaustion of the worker, a further reduction of working hours must soon become inevitable; the eight-hour agitation has begun.",
  "5.3", ""),
 ("A growing servant class", "forecast", F, "yes", ["5.13"],
  "Rising productivity lets an ever larger share of the working class be employed unproductively, especially as domestic servants (more numerous in 1861 than textile and mine workers combined).",
  "5.13", ""),
 ("Boom and bust as the normal life of industry", "forecast", D, "yes", ["5.15"],
  "Modern industry's capacity for sudden expansion, together with dependence on world markets, produces a cycle of moderate activity, prosperity, overproduction, crisis and stagnation; insecure employment becomes normal, and wages are cut in downturns.",
  "5.15", "Marx elsewhere calls the cycle 'decennial' (ch25)."),
 ("Industrial centers versus raw-material suppliers", "implicit_argument", W, "yes", ["5.16"],
  "Cheap machine goods and transport let industrial countries ruin handicrafts abroad and turn other countries into suppliers of raw materials (India for cotton, Australia for wool), creating a new international division of labor.",
  "5.16", "Engels notes the US had since industrialized."),
 ("The education of the future combines work and schooling", "forecast", F, "yes", ["5.21"],
  "The factory system contains the germ of the future education, combining productive labor with instruction and gymnastics for every child above a certain age, both to raise production and as the only way to produce fully developed people.",
  "5.21", ""),
 ("Industry will demand adaptable, all-round workers", "forecast", F, "yes", ["5.22"],
  "Because modern industry constantly revolutionizes production, it makes variation of work and worker mobility a condition of survival, compelling society to replace the detail worker with the fully developed individual, though in capitalist form it reproduces the old division of labor.",
  "5.22", ""),
 ("Higher form of the family", "forecast", W, "no", ["5.24"],
  "By drawing women and children into socially organized production, modern industry dissolves the old family but creates the economic foundation for a higher form of family and relations between the sexes.",
  "5.24", ""),
 ("Capitalist agriculture annihilates the peasantry", "forecast", F, "yes", ["6.4", "8.9"],
  "Modern industry in agriculture destroys the peasant and replaces him with the wage laborer, concentrates population in towns and, with machinery, radically expropriates the great majority of the rural population.",
  "6.4", ""),
 ("Capitalist agriculture robs the soil", "forecast", W, "yes", ["6.5"],
  "By concentrating people in towns, capitalist agriculture disturbs the circulation of matter between people and soil, breaking the conditions of lasting fertility; every advance in it is progress in robbing both the worker and the soil, fastest in new countries like the United States.",
  "6.5", "Relies on Liebig."),
 ("Rising productivity widens the gap between workers and capitalists", "implicit_argument", W, "yes", ["6.9", "7.6", "7.19"],
  "Even if workers consume more, productivity gains raise surplus-value, so the gap between worker and capitalist keeps widening; real wages never rise in proportion to productivity. A working class that is merely 'less poor' while the rich grow much richer stays relatively as poor.",
  "7.6", "A claim about relative, not absolute, position."),
 ("Wage form hides unpaid labor", "theme", D, "no", ["6.12", "6.18", "6.19", "6.23"],
  "The wage appears to pay for all labor, hiding the split between paid and unpaid labor; continued production reproduces the capital relation itself, turns every capital into capitalized unpaid labor, and turns the property laws of commodity exchange into laws of capitalist appropriation.",
  "6.12", ""),
 ("Hourly pay, irregular hours and the overtime trap", "implicit_argument", D, "yes", ["6.13", "6.14"],
  "Pay by the hour without guaranteed hours lets employers break the link between paid and unpaid time, alternate overwork with idleness, and destroy regular employment; low hourly rates push workers into long hours, and the longer the hours in a trade, the lower the wages.",
  "6.13", ""),
 ("Piece-work fosters intensity, subcontracting and lower average pay", "implicit_argument", D, "yes", ["6.15"],
  "Piece wages measure intensity for the employer, make supervision unnecessary, underlie outwork and subcontracted sweating, and, by setting workers in competition, tend to lower the average wage while raising some individuals' pay.",
  "6.15", ""),
 ("High wages in productive countries do not mean high labor costs", "implicit_argument", D, "yes", ["6.17"],
  "Countries with more developed capitalism have higher productivity and intensity, hence higher money wages, but the price of labor relative to output or surplus-value can be lower there.",
  "6.17", ""),
 ("Employers treat trained workers as their property", "implicit_argument", D, "yes", ["6.21", "6.20"],
  "During the cotton famine manufacturers treated skilled operatives as their 'living machinery' and opposed their emigration; capital wants workers' consumption limited to what reproduces labor-power.",
  "6.21", ""),
 ("Wealth increasingly belongs to those who appropriate others' labor", "forecast", F, "yes", ["6.24", "7.20"],
  "In the capitalist period social wealth becomes to an ever-increasing degree the property of those able to appropriate others' unpaid labor; English tax data of 1851-66 show incomes from profits concentrating at the top.",
  "6.24", ""),
 ("Capital pushes wages toward zero", "implicit_argument", W, "yes", ["7.5"],
  "Capital constantly tends to push labor costs toward an unreachable zero, including by paying below the value of labor-power (with poor relief topping up wages, as under Speenhamland), converting workers' consumption fund into accumulation.",
  "7.5", "A 3rd-edition note adds the claim that European wages are being pressed toward Chinese levels."),
 ("The share of machinery and materials in capital keeps rising", "forecast", F, "yes", ["7.8", "2.15"],
  "As accumulation and productivity grow, means of production grow faster than labor-power (the technical and organic composition of capital rise), so demand for labor falls relative to total capital, even if it rises absolutely.",
  "7.8", "Marx notes cheaper means of production mean the value composition rises more slowly than the technical one."),
 ("Overwork and unemployment feed each other", "implicit_argument", D, "yes", ["7.12"],
  "Overwork of the employed swells the reserve army, whose competition forces the employed into overwork; a rationally shortened working day would need nearly the whole working population to maintain current output.",
  "7.12", ""),
 ("The poor have larger families and shorter lives", "implicit_argument", D, "yes", ["7.16"],
  "Births and family size vary inversely with wages, and the lowest layers renew a quickly used-up working population with large families; life expectancy differs sharply by class.",
  "7.16", ""),
 ("The general law: wealth at one pole, misery at the other", "forecast", F, "yes", ["7.17"],
  "The greater social wealth and capital, the larger the reserve army and official pauperism; accumulation of wealth at one pole is accumulation of misery, toil, ignorance and degradation at the other, and the worker's lot, whatever his pay, must grow worse. Marx adds that the law is modified by many circumstances.",
  "7.17", "Readers dispute whether 'worse' is absolute or relative; the text's 'be his payment high or low' blocks the simple real-wage test."),
 ("Housing for workers worsens as accumulation speeds up", "implicit_argument", D, "yes", ["7.21"],
  "The faster capital accumulates, the worse workers' housing; urban 'improvements' (banks, roads, railways) push the poor into more crowded quarters while landlords profit, and sanitary laws only move overcrowding elsewhere.",
  "7.21", ""),
 ("Farm output rises while farm workers dwindle and suffer", "implicit_argument", D, "yes", ["7.23", "8.23", "8.24", "7.24"],
  "Drainage, machinery and bigger farms raised output and rents while agricultural laborers fell in number and their lot worsened; cottages were razed and gangs of women and children kept adult men's wages down; official surveys found workers' diets below the subsistence minimum.",
  "7.23", ""),
 ("Open force first, then the 'dull compulsion' of economics", "implicit_argument", D, "yes", ["8.5", "8.6", "8.7"],
  "The expropriated were driven into wage discipline by brutal laws against vagabondage; wage laws set maximums but no minimums and banned unions, making Parliament a 'permanent Trades' Union of the capitalists'. Once capitalism matures, economic necessity does the work and direct force is used only exceptionally.",
  "8.6", ""),
 ("Colonies, slavery, public debt and tariffs as levers of early capitalism", "implicit_argument", D, "yes", ["8.10", "8.13"],
  "Colonial plunder, slavery, national debt, modern taxation and protectionism were the chief means of primitive accumulation, combined in England by the late 17th century; force is the midwife of a new society. Wage labor in Europe rested on outright slavery in the New World.",
  "8.10", "Historians remain divided on the size of slavery's contribution (Williams thesis debate)."),
 ("Public debt breeds a financial aristocracy and ever-rising taxes", "implicit_argument", W, "yes", ["8.11"],
  "National debt lets money earn without risk, creating rentiers, financiers and stock-market gambling; with taxes on necessities it carries the seed of automatic progression, so overtaxation is a principle, not an accident.",
  "8.11", ""),
 ("The expropriators will be expropriated", "forecast", F, "yes", ["8.16", "5.23", "6.2", "7.1"],
  "Centralization of the means of production and socialization of labor reach a point where they no longer fit their capitalist shell, which bursts: 'the expropriators are expropriated'. The working class will come to power, which Marx calls inevitable, and the result is individual property based on co-operation and common possession of land and means of production.",
  "8.16", "The book's best-known forecast. Marx gives no date; the 'negation of the negation' framing is dialectical."),
 ("Growing misery brings an organized working-class revolt", "forecast", F, "yes", ["8.15"],
  "As the number of capital magnates shrinks, the mass of misery, oppression and exploitation grows, and so does the revolt of a working class ever larger and disciplined, united and organized by capitalist production itself.",
  "8.15", ""),
 ("Socializing capitalist property will be easier than its creation", "forecast", F, "yes", ["8.17"],
  "Turning capitalist property, which already rests on socialized production, into social property will be incomparably less long, violent and difficult than the original expropriation of the many by the few.",
  "8.17", "Conditional on such a transition happening."),
 ("Where land is free, capital cannot find workers", "implicit_argument", D, "yes", ["8.18", "8.21"],
  "In colonies with free land, workers become independent producers and capital cannot exploit them, showing capital is a social relation, not a thing. Similarly, Ireland's mass emigration did not cure poverty because relative surplus population kept pace with depopulation.",
  "8.18", "The opposing views are O23 (Wakefield) and O24 (Malthusian depopulation)."),
 ("The United States is no longer a promised land for immigrants", "forecast", F, "yes", ["8.20"],
  "Mass immigration, Civil War debt and taxes, a new financial aristocracy and land grants to railways mean the United States has ceased to be the promised land for emigrant workers, and capitalist production there advances with giant strides, though wages are not yet at European levels.",
  "8.20", "Partly a present-tense observation (1860s-70s) with an implied tendency."),
]

# Claims Marx attributes to opponents (not researched as the book's claim)
OPP = [
 ("Value exists only as exchange ratios", "Bailey; Bastiat; free-traders", ["1.20"]),
 ("Every sale is a purchase, so general gluts are impossible", "Say; James Mill", ["1.21"]),
 ("Prices are set by the quantity of money", "Hume, Vanderlint, Locke, Montesquieu, Ricardo school", ["1.22"]),
 ("Money is a mere symbol with imaginary value", "Locke; Law; royal jurists", ["1.23"]),
 ("Bourgeois institutions are natural; feudal ones artificial", "Bastiat; classical economists", ["1.24"]),
 ("Exchange or commerce creates value", "Condillac; Newman; Destutt de Tracy", ["2.4"]),
 ("Profit comes from consumers paying above value", "Torrens; Malthus", ["2.5"]),
 ("Profit rewards the capitalist's abstinence, risk or superintending labor", "Senior; Roscher; Say; MacCulloch", ["2.12", "2.24", "3.19", "7.2", "2.2"]),
 ("All net profit comes from the 'last hour'", "Nassau Senior", ["3.18"]),
 ("Restricting night work or meal times would ruin industry; shorter hours must cut output", "Manufacturers; early Horner", ["3.20", "5.5"]),
 ("Workers are lazy; low wages compel six days' work", "Essay on Trade and Commerce (1770); Arthur Young", ["3.21"]),
 ("Child labor is old; only humane remedies are new", "Macaulay", ["3.22"]),
 ("Workers themselves want the long day", "Lancashire manufacturers (1848)", ["3.23"]),
 ("Only net revenue matters, not how many it employs", "Ricardo", ["3.24"]),
 ("Displaced workers are automatically re-employed (compensation theory)", "James Mill, MacCulloch, Torrens, Senior, J. S. Mill", ["5.10"]),
 ("Machinery is blameless; only misuse harms workers", "MacCulloch and apologists", ["5.11", "4.21"]),
 ("Science will always teach labor docility; the factory brings order", "Ure", ["5.7", "4.23", "5.1"]),
 ("Profit comes from labor producing more than its support", "J. S. Mill", ["6.8"]),
 ("Workers have no claim on gains from new machinery", "Employers; Watts", ["6.16"]),
 ("A fixed wage fund divided by workers sets wages", "Bentham, Malthus, James Mill, MacCulloch, Fawcett", ["7.4", "7.3"]),
 ("Wages and population oscillate by natural law", "Malthus; Martineau", ["7.14"]),
 ("Poverty is necessary for national wealth", "Mandeville; Townsend; Storch; Destutt de Tracy", ["7.18"]),
 ("Wakefield's 'sufficient price': dear land to manufacture wage workers", "E. G. Wakefield", ["8.19"]),
 ("Misery comes from absolute overpopulation; depopulation cures it (Ireland)", "Malthusians; Lord Dufferin; Senior", ["8.21", "8.22"]),
 ("The rich became rich by thrift, the poor poor by idleness", "Adam Smith; Thiers", ["8.1"]),
 ("A nation grows richer the deeper it is in debt", "unnamed 'modern doctrine'", ["8.12"]),
 ("Belgium is the workers' paradise", "English capitalists", ["7.22"]),
 ("Public education of the masses violates the division of labor", "Garnier", ["4.22"]),
 ("Machines render value-creating 'services'", "Say (Ricardo partly)", ["4.24"]),
 ("Free labor market as an Eden of freedom and equality", "Rossi; free-trade vulgarians", ["2.10"]),
]

def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[*_]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()

def chapter_text(ids):
    files = {anchors[a]["file"] for a in ids if a in anchors}
    return norm(" ".join((root / "original" / f).read_text() for f in files))

natkey = lambda a: (a.split("-p")[0], int(a.split("-p")[1]))
out, problems = [], []
for n, (title, kind, spec, testable, srcs, claim, qsrc, note) in enumerate(ITEMS, 1):
    tid = f"T{n:02d}"
    anc = []
    for s in srcs:
        for a in cands[s]["anchors"]:
            if a not in anc: anc.append(a)
    for a in anc:
        if a not in anchors: problems.append(f"{tid}: bad anchor {a}")
    anc = sorted([a for a in anc if a in anchors], key=natkey)
    q = cands[qsrc]["quote"] if qsrc else ""
    if q:
        frag = norm(q.split("...")[0])
        if frag not in chapter_text(cands[qsrc]["anchors"]): problems.append(f"{tid}: quote not found: {q}")
    speaker = "Engels (editorial note)" if "Engels, in a note" in note else "Marx"
    out.append({"id": tid, "title": title, "kind": kind, "speaker": speaker, "specificity": spec, "testable": testable,
                "claim": claim, "quote": q, "quote_anchor": cands[qsrc]["anchors"][0] if q else "",
                "anchors": anc, "note": note, "sources": srcs,
                "verdict": "too_vague_to_judge" if testable == "no" else None})
opp = []
for n, (title, who, srcs) in enumerate(OPP, 1):
    anc = sorted({a for s in srcs for a in cands[s]["anchors"] if a in anchors}, key=natkey)
    opp.append({"id": f"O{n:02d}", "title": title, "attributed_to": who, "anchors": anc, "sources": srcs,
                "marx_response": cands[srcs[0]]["claim"]})
used = {s for it in ITEMS for s in it[4]} | {s for o in OPP for s in o[2]}
unused = sorted(set(cands) - used, key=lambda k: tuple(map(int, k.split("."))))
print("unused candidates:", unused)
print("\n".join(problems) or "quotes and anchors OK")
(root / "themes-index.json").write_text(json.dumps({"items": out, "opponent_claims": opp}, indent=1, ensure_ascii=False))

from collections import Counter
c = Counter((i["specificity"], i["testable"]) for i in out)
L = ["# Capital, Vol. 1: Themes Index", "",
     "Built from `original/` only. Every anchor is a paragraph ID from `anchors.json`. "
     "T-items are claims the book makes in Marx's own voice (one, T13, is an editorial note by Engels and is marked so). "
     "O-items are views Marx attributes to opponents in order to answer them; they are listed so they are never read as the book's claim, and are not researched.", "",
     "**Specificity:** concrete_forecast (a definite future development) · general_warning (a tendency or danger stated loosely) · described_pattern (how things work or worked). "
     "**Testable: no** means almost any outcome would fit; those items have their verdict pre-set to `too_vague_to_judge` and are not researched.", "",
     "## Counts", "", "| Specificity | Testable | Not testable | Total |", "|---|---|---|---|"]
for s in (F, W, D):
    L.append(f"| {s} | {c[(s,'yes')]} | {c[(s,'no')]} | {c[(s,'yes')]+c[(s,'no')]} |")
L += [f"| **all** | {sum(v for k,v in c.items() if k[1]=='yes')} | {sum(v for k,v in c.items() if k[1]=='no')} | {len(out)} |", "",
      f"Plus {len(opp)} opponent claims (O01–O{len(opp):02d}).", "",
      "## Major themes", ""]
L += ["Each major theme with the T-items (and so the anchors) that carry it:", "",
      "- **Value, money and fetishism:** T01–T14",
      "- **Capital and accumulation:** T16, T17, T39, T40, T58, T63, T65",
      "- **The working day and its regulation:** T20–T32, T38, T47, T48, T66",
      "- **Division of labor and machinery:** T33, T35–T37, T41–T46, T52, T53",
      "- **Wages:** T19, T57, T59–T62, T64",
      "- **Reserve army, inequality and living conditions:** T34, T49, T50, T67–T69",
      "- **Agriculture and the soil:** T15, T55, T56, T70",
      "- **Primitive accumulation, colonies and the state:** T18, T24, T51, T71–T73, T77, T78",
      "- **Where capitalism leads:** T54, T74–T76", "",
      "## Items", ""]
for i in out:
    L.append(f"### {i['id']} · {i['title']}")
    tag = f"`{i['specificity']}` · testable: **{i['testable']}** · {i['kind'].replace('_',' ')}"
    if i["speaker"] != "Marx": tag += f" · speaker: **{i['speaker']}**"
    if i["verdict"]: tag += f" · verdict: `{i['verdict']}`"
    L.append(tag + "  ")
    L.append(i["claim"] + "  ")
    if i["quote"]: L.append(f"Quote: “{i['quote']}” ({i['quote_anchor']})  ")
    L.append("Anchors: " + ", ".join(i["anchors"]) + ("  " if i["note"] else ""))
    if i["note"]: L.append("Note: " + i["note"])
    L.append("")
L += ["## Opponent claims (not the book's claim; not researched)", ""]
for o in opp:
    L.append(f"- **{o['id']} · {o['title']}** ({o['attributed_to']}). Anchors: {', '.join(o['anchors'][:6])}")
(root / "themes-index.md").write_text("\n".join(L) + "\n")
print(c, len(out), len(opp))
