import ROOT
import numpy as np
import os.path
import itertools
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#dir1 = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/ntuples/14_11_2023_01_59_28/" # scale 1.0
#dir1 = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/ntuples/15_11_2023_22_25_51/" # scale 1.0 wiht more events

#bkg
dir1Bkg = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/ntuples/16_11_2023_09_42_50/" # scale 1.0 with even more events ;)
dir2Bkg = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/ntuples/14_11_2023_17_23_41/" # scale 2.0 only need 1 vs 3 atm
dir3Bkg = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/ntuples/15_11_2023_11_48_13/" # scale 3.0

#signal
dir1Sig = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/ntuples/20_11_2023_09_22_20/" # scale 1.0 with even more events ;)
dir3Sig = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/ntuples/20_11_2023_22_45_59/" # scale 3.0

moms = ["b","ds","mu","kp", "km", "pi"]
variables = ["pt","eta"]

variables = list(itertools.product(moms, variables))
variables = ['_'.join(comb) for comb in variables]

labels = {
'b_pt': r'p_{T} H_{b} [GeV]',
'ds_pt':r'p_{T} D_{s}-meson [GeV]',
'mu_pt':r'p_{T} #mu [GeV]',
'kp_pt':r'p_{T} K^{+} [GeV]',
'km_pt':r'p_{T} K^{-} [GeV]',
'pi_pt':r'p_{T} #pi [GeV]',
'abs(b_eta)':r'|#eta(H_{b})|',
'abs(ds_eta)':r'|#eta(D_{s})|',
'abs(mu_eta)':r'|#eta(#mu)|',
'abs(kp_eta)':r'|#eta(K^{+})|',
'abs(km_eta)':r'|#eta(K^{-})|',
'abs(pi_eta)':r'|#eta(#pi)|',

}

def printScale(name):

  chain1 = ROOT.TChain("tree")
  chain3 = ROOT.TChain("tree")

  if name == "signal": 
    dir1 = dir1Sig
    dir3 = dir3Sig

  else:
    dir1 = dir1Bkg
    dir3 = dir3Bkg

  trees1 = os.listdir(dir1)
  trees3 = os.listdir(dir3)

  for tree in trees1:
    print("Adding ", tree, " to chain")
    chain1.Add(dir1 + tree)

  for tree in trees3:
    print("Adding ", tree, " to chain")
    chain3.Add(dir3 + tree)

  chains = [chain1,chain3]


  for var in variables:

        if 'eta' in var: var = 'abs(' + var + ')'
 
        maxx = max([chains[0].GetMaximum(var),chains[1].GetMaximum(var)])
        if var == 'pi_pt': maxx = 40


        print "Start filling " + var + " histogram; Events to fill: " + str(chains[0].GetEntries() + chains[1].GetEntries())
    
        #dummy

        h = ROOT.TH1D("","",50,0,maxx)
        h.GetYaxis().SetTitle('a.u.')
        h.GetXaxis().SetTitle(var)
        h.GetXaxis().SetTitle(labels[var])
 
        h1 = h.Clone()
        h1.SetName("1")
        h1.SetLineColor(ROOT.kBlue)
        h1.SetLineWidth(2)

        h3 = h.Clone()
        h3.SetName("3")
        h3.SetLineColor(ROOT.kRed)
        h3.SetLineWidth(2)
       
        chains[0].Project("1",var)
        chains[1].Project("3",var)
       
        n1 = h1.Integral()
        n1e = h1.GetEntries()
        n3 = h3.Integral()
        n3e = h3.GetEntries()
        print(n1,n1e,n3,n3e)

        h1.Scale(1/h1.Integral())
        h3.Scale(1/h3.Integral())

        yMax = max([h1.GetMaximum(),h3.GetMaximum()])
        h1.SetMaximum(yMax*1.2)
        
        #KS test
        ks_score = h1.KolmogorovTest(h3)
        ks_value = ROOT.TPaveText(0.5, 0.8, 0.6, 0.9, 'nbNDC')
        ks_value.AddText('KS score = {0}'.format(round(ks_score,5)))
        ks_value.SetFillColor(0)
        ks_value.SetFillStyle(0)
        ks_value.SetBorderSize(0)
        ks_value.SetTextFont(42)
        ks_value.SetTextSize(0.04)
        
        ROOT.gStyle.SetOptStat(0)
        c1 = ROOT.TCanvas("canvas", "Canvas", 800, 600)
        leg = ROOT.TLegend(0.7,0.8,0.8,0.9);
        leg.SetBorderSize(0)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(42)
        leg.SetTextSize(0.04)
        
        #h1.Draw("EP")
        h1.Draw("HIST ")
        leg.AddEntry(h1," Scale = 1.0", 'l')
        #h3.Draw('EP SAME')
        h3.Draw('HIST SAME')
        leg.AddEntry(h3," Scale = 3.0", 'l')
        
        ks_value.Draw('EP same')
        leg.Draw("SAME")
        
        c1.Update()
        c1.Modified()
        
        if 'eta' in var: var = var[4:-1]
        c1.SaveAs("./scaleplots/scaletofilter_{0}_{1}.png".format(name,var))

printScale("signal")
printScale("bkg")

