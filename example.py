from pyflipt import get_client
from pyflipt import Flag, Segment, Constraint, Rule, ComparisonType, MatchType, OperatorType
import asyncio


async def main():
    pf = get_client()
    flag = Flag(key="collectors", name="Collectors", enabled=True)
    await pf.create(flag)

    segments = [
        Segment(key="user", name="Selected users",  match_type=MatchType.ANY.value),
        Segment(key="account", name="Selected accounts",  match_type=MatchType.ANY.value),
        Segment(key="datasource_uuid", name="Selected datasources",  match_type=MatchType.ANY.value),
    ]
    for segment in segments.values():
        await pf.create(segment)

    constraints = [
        Constraint(segment_key="user", type=ComparisonType.STRING.value, operator=OperatorType.EQ, value="test.admin@onna.com"),
        Constraint(key="datasource_uuid", type=ComparisonType.STRING.value, operator=OperatorType.EQ, value="foobar"),
        Constraint(key="account", type=ComparisonType.STRING.value, operator=OperatorType.EQ, value="account1"),
    ]
    for constraint in constraints:
        await pf.create(constraint)

    rules = []
    for rank, segment in enumerate(segments):
        rules.append(
            Rule(flag_key=flag.key, segment_key=segment.key, rank=rank)
        )
    for rule in rules:
        pf.create(rule)


if __name__ == "__main__":
    asyncio.run(main)
