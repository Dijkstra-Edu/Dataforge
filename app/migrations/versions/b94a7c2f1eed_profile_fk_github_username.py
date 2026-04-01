"""Profile FK via github username; drop user_id

Revision ID: b94a7c2f1eed
Revises: 3729235ae6dd
Create Date: 2026-03-28

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

# revision identifiers, used by Alembic.
revision: str = "b94a7c2f1eed"
down_revision: Union[str, Sequence[str], None] = "3729235ae6dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    op.execute(
        sa.text(
            """
            UPDATE "Profile" AS p
            SET username = u.github_user_name
            FROM "User" AS u
            WHERE p.user_id = u.id
            """
        )
    )

    remaining = bind.execute(
        sa.text('SELECT COUNT(*) FROM "Profile" WHERE username IS NULL')
    ).scalar()
    if remaining and remaining > 0:
        raise RuntimeError(
            f"{remaining} Profile row(s) still have NULL username after backfill; fix data and retry."
        )

    op.alter_column(
        "Profile",
        "username",
        existing_type=sqlmodel.sql.sqltypes.AutoString(),
        nullable=False,
    )

    insp = sa.inspect(bind)
    fk_names = [
        fk["name"]
        for fk in insp.get_foreign_keys("Profile")
        if "user_id" in (fk.get("constrained_columns") or [])
    ]
    for name in fk_names:
        op.drop_constraint(name, "Profile", type_="foreignkey")

    uq_names = [
        uq["name"]
        for uq in insp.get_unique_constraints("Profile")
        if list(uq.get("column_names") or []) == ["user_id"]
    ]
    for name in uq_names:
        op.drop_constraint(name, "Profile", type_="unique")

    op.drop_column("Profile", "user_id")

    op.create_foreign_key(
        "fk_profile_username_refs_user_github_user_name",
        "Profile",
        "User",
        ["username"],
        ["github_user_name"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )


def downgrade() -> None:
    bind = op.get_bind()

    op.drop_constraint(
        "fk_profile_username_refs_user_github_user_name",
        "Profile",
        type_="foreignkey",
    )

    op.add_column(
        "Profile",
        sa.Column("user_id", sa.Uuid(), nullable=True),
    )

    op.execute(
        sa.text(
            """
            UPDATE "Profile" AS p
            SET user_id = u.id
            FROM "User" AS u
            WHERE p.username = u.github_user_name
            """
        )
    )

    remaining = bind.execute(
        sa.text('SELECT COUNT(*) FROM "Profile" WHERE user_id IS NULL')
    ).scalar()
    if remaining and remaining > 0:
        raise RuntimeError(
            f"{remaining} Profile row(s) could not restore user_id; fix data and retry downgrade."
        )

    op.alter_column("Profile", "user_id", nullable=False)
    op.create_unique_constraint(
        "uq_profile_user_id_restore",
        "Profile",
        ["user_id"],
    )
    op.create_foreign_key(
        "fk_profile_user_id_restore_user_id",
        "Profile",
        "User",
        ["user_id"],
        ["id"],
    )
