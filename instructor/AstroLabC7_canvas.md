# AstroLab C7: Canvas Checkpoint Questions

Multiple-choice questions for building the H5P quiz on Canvas. The correct answer is marked ✅, and each question has feedback you can show for a wrong answer. Students get unlimited attempts and marks are for completion.

> ⚠️ **Before going public:** this folder holds the answers. Move it to a private location (or delete it) before making the repository public.

> ⏳ **Pending data:** Q5 and Q7 depend on the final GRB and 2MASS catalogues. The values below are what's expected for an isotropic sample and will be confirmed once the data files are added.

---

## Q1. Light from the Sun (Part 1)

How long does light take to travel from the Sun to the Earth?

- [ ] 8.3 seconds
- [x] ✅ 8.3 minutes
- [ ] 8.3 hours
- [ ] 8.3 days

**Feedback:** Divide the distance (1 AU) by the speed of light and convert to minutes: `(1 * u.AU / c).to(u.min)`.

---

## Q2. Proxima Centauri in parsecs (Part 1)

Using the distance converter, how far away is Proxima Centauri in parsecs?

- [ ] 0.77 pc
- [x] ✅ 1.30 pc
- [ ] 4.25 pc
- [ ] 13.9 pc

**Feedback:** Choose Proxima Centauri and parsecs in the converter. One parsec is about 3.26 light-years, so 4.25 ly is about 1.30 pc.

---

## Q3. Lookback time to MoM-z14 (Part 1)

Light from MoM-z14 has been travelling for about 13.5 billion years, and the Universe is about 13.8 billion years old. Roughly how old was the Universe when that light set off?

- [ ] About 3 million years
- [x] ✅ About 300 million years
- [ ] About 3 billion years
- [ ] About 13.5 billion years

**Feedback:** Subtract the travel time from the age of the Universe: 13.8 − 13.53 ≈ 0.27 billion years, or roughly 300 million years. The lecture quotes 280 million years.

---

## Q4. Powers of ten (Part 2)

How many orders of magnitude separate the distance to the Moon from the distance to MoM-z14?

- [ ] 5.6
- [ ] 12.0
- [x] ✅ 17.5
- [ ] 23.1

**Feedback:** Run the cell that computes `np.log10(ratio)`. 5.6 and 23.1 are the powers of ten of each distance in km on their own; the difference between them is 17.5.

---

## Q5. GRBs above the Milky Way plane (Part 3)

What fraction of the BATSE gamma-ray bursts are above the plane of the Milky Way?

- [ ] About 0.10
- [ ] About 0.25
- [x] ✅ About 0.50
- [ ] About 0.90

**Feedback:** Run the cell that calculates `fraction_north`. About half are above and half below, which is what we'd expect if GRBs are spread evenly across the sky.

---

## Q6. Which dataset is the most isotropic? (Part 3)

- [ ] Galaxies closer than 30 Mpc
- [ ] All the 2MASS galaxies
- [x] ✅ Gamma-ray bursts

**Feedback:** Isotropic means the same in every direction. Nearby galaxies clump into groups and clusters, and the 2MASS map has a gap where Milky Way dust blocks the view. GRBs come from billions of light-years away and gamma rays pass through the dust, so they're spread evenly over the whole sky.

---

## Q7. Including more distant galaxies (Part 3)

As you include more distant galaxies with the slider, what happens to the fraction above the Milky Way plane?

- [ ] It moves further away from 0.50
- [x] ✅ It gets closer to 0.50
- [ ] It drops to zero
- [ ] It doesn't change at all

**Feedback:** On small scales the Universe is clumpy, so nearby galaxies are lopsided. Averaging over bigger and bigger volumes smooths out the clumps, just as the cosmological principle predicts.

---

## Q8. A static universe (Part 4)

In a static toy universe with the age set to 200, roughly what percentage of the sky is covered by stars?

- [ ] About 10%
- [ ] About 50%
- [ ] About 75%
- [x] ✅ About 100%

**Feedback:** If the Universe is old enough (or infinite), every line of sight eventually ends on a star, like trees in a forest. That's Olbers' paradox: the sky should be as bright as the surface of a star.

---

## Q9. An expanding universe (Part 4)

With the age at 200, tick "Expanding universe". What happens, and why?

- [ ] The sky gets brighter, because there are more stars
- [ ] The sky stays the same, because the stars haven't moved
- [x] ✅ The sky gets much darker, because light from distant stars is redshifted and dimmed
- [ ] The stars disappear, because they've moved past the horizon

**Feedback:** The sky is still covered by stars, but expansion stretches the light from distant stars to longer wavelengths and dims it. This is one of the real resolutions of Olbers' paradox, along with the finite age of the Universe.

---

## Q10. Image stretches (Part 5)

With the clip slider at 100%, which stretch makes the galaxy almost invisible?

- [x] ✅ Linear
- [ ] Square root
- [ ] Logarithmic
- [ ] Asinh

**Feedback:** A few pixels (bright stars and the galaxy's core) are thousands of times brighter than everything else. A linear stretch spends almost all its range on them, so the faint parts look black. Log and asinh stretches compress the bright end so faint detail shows up, just like the zscale option in SAOImageDS9.
