# Full study reports and admission limits

The four PDFs are public mirror copies of reports bearing OSUAH/SECTRA attribution. manifest.json records the exact Drive source and SHA256. The Drive owner's identity has not been independently verified; content attribution is not proof of official hosting. Full ZIP remains local and is ignored; four PDFs individually below50MB are archived. Each PDF hash was checked against the acquisition manifest.

Verified report passages (printed pagination):

- Final VolI p83,sections4.2.4–4.2.5: household interview followed by an assigned diary day; complete-household journey responses; final questionnaire approvedJune2012 and field implementation fromJuly2012. This section does not reproduce the exact Estudios/Curso questions.
- Final VolI p102–103 and VolII p48–50: origin/destination geocoding may use street addresses, intersections or reference landmarks, converted to UTM. Hence even exact coordinate equality does not independently prove household-origin identity. Our coordinate-based commute records remain conditional, not confirmed observed household departures.
- Final VolII p42,section8.6.3: person weights start from household weights and adjust for municipality age/sex distributions and projected population totals. This supports person-weight rather than trip-weight aggregation for a person estimand; it does not establish the downloaded weight vintage or high-school representativeness.
- Final VolII p173: school-enrolment consistency checks use age categories and acknowledge older school students, outside-area trips and absence. This does not identify Estudios as current enrollment.

No original Estudios/Curso wording was located in the report text. Exact current high-school classification remains unresolved. Conditional trip-chain scenarios retain full unknown intervals for missing cases and are not admitted to the city model. Previous descriptions of 'confirmed' coordinate-only origins should be read as passing an algorithmic matching rule, not independent proof of home origin.

Current mathematical model remains S=100sqrt(B)/(sqrt(A)+sqrt(B)), B=sum(w*u²), A=sum(w*(1-u)²). Conditional commute missingness bounds are sum(person_weight*lower_or_upper_utility)/sum(person_weight), with utility exp(-minutes/30) only where scenario rules accept a duration. No main ranking rerun is justified by this document-only evidence update.
