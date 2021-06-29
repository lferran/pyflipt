from pyflipt import get_client
from pyflipt import Flag, Segment, Constraint, Rule, ComparisonType, MatchType, OperatorType
import asyncio

FLIPT_API_BASE_URL = "http://localhost:8083/api/v1"


async def main():
    pf = get_client(FLIPT_API_BASE_URL)

    flag = Flag(key="collectors3", name="Collectors", enabled=True)
    await pf.create(flag)

    segments = [
        Segment(key="user", name="Selected users",  match_type=MatchType.ANY.value),
        Segment(key="account", name="Selected accounts",  match_type=MatchType.ANY.value),
        Segment(key="datasource_uuid", name="Selected datasources",  match_type=MatchType.ANY.value),
    ]
    for segment in segments:
        await pf.create(segment)

    constraints = [
        Constraint(segment_key=segments[0].key, type=ComparisonType.STRING.value, property="user", operator=OperatorType.EQ, value="test.admin@onna.com"),
        Constraint(segment_key=segments[1].key, type=ComparisonType.STRING.value, property="account", operator=OperatorType.EQ, value="account1"),
        Constraint(segment_key=segments[2].key, type=ComparisonType.STRING.value, property="datasource_uuid", operator=OperatorType.EQ, value="foobar"),
    ]
    for constraint in constraints:
        await pf.create(constraint)

    rules = []
    for rank, segment in enumerate(segments):
        rules.append(
            Rule(flag_key=flag.key, segment_key=segment.key, rank=rank + 1)
        )
    for rule in rules:
        await pf.create(rule)

    await pf.close()

if __name__ == "__main__":
    asyncio.run(main())
