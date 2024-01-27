import pytest
from http import HTTPStatus
from uuid import uuid4
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from . import settings, Base, Role


engine = create_engine(settings.db_dsn, echo=False)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# test 1: New role adding
@pytest.mark.parametrize(
    'test_data, query_data, expected_answer',
    [
        # new role
        (
                {},
                {'name': 'premium'},
                {'status_code': HTTPStatus.OK,
                 'body': {
                     'name': 'premium',
                 },
                 }
        ),

        # added role
        (
                {
                    'uuid': uuid4(),
                    'name': 'premium'
                },
                {'name': 'premium'},
                {'status_code': HTTPStatus.BAD_REQUEST,
                 'body': {'detail': 'Role already exist'},
                 }
        ),

    ]
)
@pytest.mark.asyncio
async def test_add_new_role(db_session, make_post_request,
                            test_data: dict,
                            query_data: dict,
                            expected_answer: dict,
                            ):
    """Test add new role"""

    try:

        if test_data:
            new_role = Role(**test_data)
            db_session.add(new_role)
            db_session.commit()

        status, body, _ = await make_post_request(endpoint='/api/v1/',
                                                  params=query_data)

        assert status == expected_answer['status_code']

        if status == HTTPStatus.OK:

            assert body['name'] == expected_answer['body']['name']

            query = select(Role).where(Role.name == query_data['name'])
            res = db_session.execute(query)
            db_record = res.scalars().one()

            assert db_record.name == body['name']
            assert str(db_record.uuid) == str(body['uuid'])

        else:
            assert body == expected_answer['body']

    finally:

        db_session.query(Role).delete()
        db_session.commit()


# test 2: Get existing role
@pytest.mark.parametrize(
    'test_data, query_params, expected_answer',
    [
        # existing role
        (
                {
                    'uuid': 'ac58efef-be6f-410f-add8-d3ce339739f0',
                    'name': 'premium'
                },
                {'role_id': 'ac58efef-be6f-410f-add8-d3ce339739f0'},
                {'status_code': HTTPStatus.OK,
                 'body': {
                     'uuid': 'ac58efef-be6f-410f-add8-d3ce339739f0',
                     'name': 'premium'
                 },
                 }
        ),
        # not existing role
        (
                {},
                {'role_id': 'ac58efef-be6f-410f-add8-d3ce339739f0'},
                {'status_code': HTTPStatus.NOT_FOUND,
                 'body': {'detail': 'Role does not exist'},
                 }
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_role(db_session, make_get_request,
                        test_data: dict,
                        query_params: dict,
                        expected_answer: dict,
                        ):
    """Test get role"""

    try:

        if test_data:
            new_role = Role(**test_data)
            db_session.add(new_role)
            db_session.commit()

        status, body = await make_get_request(endpoint='/api/v1/',
                                              params=query_params,
                                              )

        assert status == expected_answer['status_code']
        assert body == expected_answer['body']

        if status == HTTPStatus.OK:
            query = select(Role).where(Role.name == test_data['name'])
            res = db_session.execute(query)
            db_record = res.scalars().one()

            assert db_record.name == body['name']
            assert str(db_record.uuid) == str(body['uuid'])

    finally:

        db_session.query(Role).delete()
        db_session.commit()