from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from core import db
from core.config import Config
from core.forms import RecordCreateForm
from core.models import Record
from core.views.auth import login_required

bp = Blueprint('records', __name__, url_prefix='/records')


@bp.route('/')
def index():
    """Show all the records, order by publication date."""
    page = request.args.get('page', 1, type=int)
    records = Record.query.order_by(Record.pub_date.desc()).paginate(
        page, Config.POSTS_PER_PAGE, True
    )
    next_url = url_for('records.index', page=records.next_num) \
        if records.has_next else None
    prev_url = url_for('records.index', page=records.prev_num) \
        if records.has_prev else None

    return render_template(
        'records/index.html',
        records=records.items,
        next_url=next_url,
        prev_url=prev_url,
    )


def get_record(record_id, check_author=True):
    """Get a record by id dnd check record owner"""
    record = Record.query.get(record_id)

    if record is None:
        abort(404, f"Record id {record_id} doesn't exist.")

    if check_author and record.user_id != g.user.id:
        abort(403)

    return record


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new record for the current user."""
    form = RecordCreateForm(request.form)
    if request.method == 'POST' and form.validate():
        record = Record(description=form.description.data, user_id=g.user.id)
        db.session.add(record)
        db.session.commit()
        flash('Record create!')
        return redirect(url_for('records.index'))

    return render_template('records/create.html', form=form)


@bp.route('/<record_id>/update', methods=('GET', 'POST'))
@login_required
def update(record_id):
    """Update a new record for the current user."""
    record = get_record(record_id)
    form = RecordCreateForm(request.form, record)
    if request.method == 'POST' and form.validate():
        record.description = form.description.data
        record.user_id = g.user.id
        db.session.add(record)
        db.session.commit()
        flash('Record create!')
        return redirect(url_for('records.index'))

    return render_template('records/update.html', form=form, record_id=record_id)


@bp.route('/<record_id>/delete', methods=('POST',))
@login_required
def delete(record_id):
    """Delete a record."""
    record = get_record(record_id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('records.index'))
