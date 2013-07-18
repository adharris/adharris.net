---
title: Groundwork Basics
categories: groundwork
layout: post
---

Here I'll sketch out some ideas.

### Model Definitions

Models are built by extending a common base class.

{% highlight python %}

import groundwork as gw

class Student(gw.Base):
  name   = gw.FullName()
  dob    = gw.Date()
  gender = gw.Choice(genders)

{% endhighlight %}

This would create a model called `Student`, which would store it's data in a
table also named `student`.  Each data point on the class is an instance of
a *groundwork column*.

Groundwork prefers to use class inheritance for specialized options.  For
example, `gw.FullName` would define additional functionality for dealing
with full names.  The name itself may still be stored as string in the
database.

#### Option Lists

The `genders` option may be defined like this.

{% highlight python %}
genders    = gw.Options('gender', ["Female", "Male", "Other"])
{% endhighlight %}

This would create an database-driven option list called "gender" which start
with the 3 provided terms.  Additional options could be added later via the
web interface.

#### Basic Conditionals

It is then easy to add additional models:

{% highlight python %}
placements = gw.Options("placment_type", ['Job', 'Education'])

class Placement(gw.Base):
  type       = gw.MultiChoice(placements)
  start_date = gw.Date()
  end_date   = gw.DependentDate(after=start_date)

{% endhighlight %}

`gw.DependentDate` is an example of a column with a built in conditional.  The
idea is that the column type would have two effects:

1. `end_date` is only needed if `start_date` is present
2. The value entered for `end_date` must be after the `start_date`

#### Relationships

Of course, there needs to be some sort of relationship between students and
their placements.  This is done separately from defining the models.

{% highlight python %}
Student.owns(Placement)
{% endhighlight %}

This takes care of adding a foreign key on the Placement model back to the student,
and gives the student model a collection of placement items.
