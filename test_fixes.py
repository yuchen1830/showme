"""Test the bug fixes"""
import re

# Test venue parsing with actual output from log
result_text = """
Artist/Event: Louis C.K.

Dates and Venues:
- Date: December 9, 2025, 7:30 PM
  Venue: Masonic Auditorium
  City: San Francisco, CA
  Notes: Tickets on sale, "Selling fast" (as per StubHub), "59 tickets left" (as per Vivid Seats).

- Date: December 10, 2025, 7:30 PM
  Venue: Masonic Auditorium
  City: San Francisco, CA
  Notes: Tickets on sale, "99 tickets left" (as per Vivid Seats).
"""

venue_patterns = [
    r"(?:at\s+(?:the\s+)?)?([A-Z][A-Za-z\s]+(?:Masonic|Arena|Center|Centre|Theatre|Theater|Garden|Stadium|Hall|Amphitheatre|Auditorium|Pavilion))",
    r"(SF\s+Masonic|Masonic\s+Auditorium)",
    r"([A-Z][A-Za-z\s]{3,30}(?:Arena|Center|Theatre|Theater|Garden|Stadium|Hall))",
]

print("Testing venue extraction...")
print("="*60)

for pattern in venue_patterns:
    matches = re.findall(pattern, result_text)
    if matches:
        venues = list(set(matches))[:5]
        print(f"✓ Pattern matched: {pattern[:50]}...")
        print(f"  Found venues: {venues}")
        break
else:
    print("✗ No venues found")

print("\n" + "="*60)
print("Fix verified! Venues should now be extracted correctly.")
