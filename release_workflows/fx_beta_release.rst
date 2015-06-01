Firefox Beta Release
====================
.. seealso:: :ref:`Disclaimer <workflow_disclaimer>`

..  :caption: Beta Releases
.. actdiag::
    :desctable:
    :alt: Inter-team handoffs for Public Releases
    :name: Figure3

    {
        ship_l10n -> ship_it;
        ship_it -> build_all;
        build_all ->
        qe_1 ->
        relman_1 ->
        qe_2 ->
        push_snippets ->
        qe_3 ->
        post_release -> done;
        build_all -> push_to_mirrors -> push_snippets;

        lane releng {
            label = "RelEng";
            push_snippets [label = "push updaters live", description =
            "|push_snippets|_"];
            post_release [label = "make fully visible", description =
            "|post_release|_"];
        };


        lane relman {
            label = "Rel Mgmt";
            ship_l10n [label = "Determine L10N changesets", description
            = "|ship_l10n|_"];
            ship_it [label = "Initiate release", description =
            "|ship_it|_"];
            done [label = "Success!", description="|done|"];
        };



        lane automation {
            label = "Automated Processes";
            build_all [label = "Build everything", description =
            "|build_all|"];
            push_to_mirrors [label = "push installers to mirrors",
            description = "|push_to_mirrors|_"];
        };



        lane qe {
            label = "QE";
            qe_1 [label = "functional & local updater testing", description =
            "|qe_1|"];
            relman_1 [label = "Decide build will be a GO", description =
            "|relman_1|"];
            qe_2 [label = "cdn updater testing", description =
            "|qe_2|"];
            qe_3 [label = "verify live updaters",
            description = "|qe_3|"];
        };
    }
            

.. note::

    All "RelEng" steps in the "Description" column above are taken from
    our `checklist`__ for Firefox Releases.

__ https://wiki.mozilla.org/Releases/RelEngChecklist#Release_2

..
    Release Engineering Steps

.. |push_to_mirrors| replace:: *automatic for beta 2 on* |br|
    Push Installers and updaters to Mirrors
.. _push_to_mirrors: https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Updates#Push_to_mirrors


.. |push_snippets| replace:: **Manual email from QE initiates** |br|
    Deploy the updater artifacts to the production release site. End
    users will be offered updates at this point.
.. _push_snippets: https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Updates#Push_snippets

.. |post_release| replace::  **Manual email from QE initiates** |br|
    Do final clean up of the release, including making visible on the
    FTP servers.
.. _post_release: https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Updates_through_Shipping#Desktop_post-release

..
    Release Management Steps

.. |ship_l10n| replace:: Finalize and ship L10N 
.. _ship_l10n: https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Preparation#L10N_Changesets

.. |ship_it| replace::
    Start release via `Ship-It!`_ application
.. _ship_it: https://wiki.mozilla.org/Release:Release_Automation_on_Mercurial:Starting_a_Release#Submit_to_Ship_It

.. _`Ship-It!`: https://ship-it.mozilla.com/

.. |relman_1| replace:: **Manual email from QE initiates** |br|
    Decide if this build is acceptable, or another is needed. Restart
    process for new build.
.. |done| replace:: Everything completed for this release.

..
    Automation Steps

.. |build_all| replace::
    Automation will build installers and updaters for all locales and
    all platforms. (Progress emails are sent, some of which enable QE to
    begin phases of testing. That level of detail is not shown in this
    diagram.)

..
    Quality Engineering Steps

.. |qe_1| replace:: **initiated by automated email "Updates available on beta-localtest"** |br|
    QE tests all produced artifacts, obtained via internal links.

.. |qe_2| replace:: **initiated by automated email "Updates available on beta-cdntest"** |br|
    QE verifies installers are properly accessible, and updates are
    served via normal mechanisms.
.. |qe_3| replace:: **Manual email from RelEng initiates** |br|
    QE verifies that updates are available to end users.

.. |br| raw:: html

    <br />
